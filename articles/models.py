from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save, post_save
from .utils import find_available_slug
from django.urls import reverse

# Create your models here.


class Article(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True, null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publish = models.DateField(null=True, blank=True)

    # OVERRIDING SAVE
    # def save(self, *args, **kwargs) -> None:
    #     if self.slug is None:
    #         self.slug = slugify(self.title)

    #     return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('article-detail', kwargs={'slug': self.slug})


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
