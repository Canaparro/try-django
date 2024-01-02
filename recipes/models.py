from collections.abc import Iterable
from django.db import models
from django.conf import settings
from .utils import number_str_to_float
from recipes.validators import validate_unit_of_measure


# Create your models here.

class Recipe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    directions = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    name = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    quantity = models.CharField(max_length=50)
    unit = models.CharField(max_length=50, validators=[
                            validate_unit_of_measure])
    directions = models.TextField(blank=True, null=True)
    quantity_as_float = models.FloatField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        quantity_as_float, success = number_str_to_float(self.quantity)
        if success:
            self.quantity_as_float = quantity_as_float
        else:
            self.quantity_as_float = None
        super().save(*args, **kwargs)
