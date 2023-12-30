from collections.abc import Iterable
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.db.models.signals import pre_save, post_save

# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(blank=True, null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publish = models.DateField(null=True, blank=True)

    # def save(self, *args, **kwargs) -> None:
    #     if self.slug is None:
    #         self.slug = slugify(self.title)

    #     return super().save(*args, **kwargs)


def article_pre_save(sender, instance, *args, **kwargs):
    print('pre_save')
    if instance.slug is None:
        instance.slug = slugify(instance.title)

pre_save.connect(article_pre_save, sender=Article)

def article_post_save(*args, **kwargs):
    print('post_save')

post_save.connect(article_post_save, sender=Article)