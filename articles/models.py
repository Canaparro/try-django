from django.db import models
from django.db.models.query import QuerySet
from django.utils.text import slugify
from django.db.models.signals import pre_save, post_save
from .utils import find_available_slug
from django.urls import reverse
from django.db.models import Q
from django.conf import settings

User = settings.AUTH_USER_MODEL
# Create your models here.


class ArticleQuerySet(models.QuerySet):
    def search(self, query=None):
        if query is None or query == '':
            return self.none()
        lookups = Q(title__icontains=query) | Q(content__icontains=query)
        return self.filter(lookups)


class ArticleManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return ArticleQuerySet(self.model, using=self._db)

    def search(self, query):
        return self.get_queryset().search(query)


class Article(models.Model):
    user = models.ForeignKey(User, blank=True,
                             null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True, null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publish = models.DateField(null=True, blank=True)

    objects = ArticleManager()

    # OVERRIDING SAVE
    # def save(self, *args, **kwargs) -> None:
    #     if self.slug is None:
    #         self.slug = slugify(self.title)

    #     return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('articles:detail', kwargs={'slug': self.slug})


def slugify_instance_title(instance: Article) -> Article:
    return find_available_slug(instance, slugify(instance.title))


def article_pre_save(sender, instance: Article, *args, **kwargs):
    if instance.slug is None:
        instance.slug = slugify_instance_title(instance)


pre_save.connect(article_pre_save, sender=Article)


def article_post_save(*args, **kwargs):
    # print('post_save')
    pass


post_save.connect(article_post_save, sender=Article)
