from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Recipe, RecipeIngredient

# Create your tests here.
User = get_user_model()


class UserTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('cfe', password='abc123')

    def test_user_pwd(self):
        self.assertTrue(self.user.check_password('abc123'))


class RecipeTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('cfe', password='abc123')
        self.recipe_b = Recipe.objects.create(
            name='Grilled chicken tacos', user=self.user)
        self.recipe_b = Recipe.objects.create(
            name='Grilled chicken standard', user=self.user)
        self.recipe_ingredient_a = RecipeIngredient.objects.create(
            name='Grilled chicken', quantity='1/2', unit='pound', recipe=self.recipe_b)

    def test_user_recipe_reverse_count(self):
        qs = self.user.recipe_set.all()
        self.assertEqual(qs.count(), 2)

    def test_user_recipe_forward_count(self):
        qs = Recipe.objects.all()
        self.assertEqual(qs.count(), 2)

    def test_user_recipe_ingredient_reverse_count(self):
        qs = self.recipe_b.recipeingredient_set.all()
        self.assertEqual(qs.count(), 1)

    def test_user_recipe_ingredient_count(self):
        qs = RecipeIngredient.objects.filter(recipe=self.recipe_b)
        self.assertEqual(qs.count(), 1)

    def test_user_two_level_relation(self):
        qs = RecipeIngredient.objects.filter(recipe__user=self.user)
        self.assertEqual(qs.count(), 1)

    def test_user_two_level_reverse_relation(self):
        recipeingredient_id_list = list(
            self.user.recipe_set.all().values_list('recipeingredient__id', flat=True))
        qs = RecipeIngredient.objects.filter(id__in=recipeingredient_id_list)
        self.assertEqual(qs.count(), 1)

    def test_user_two_level_relation_via_recipes(self):
        ids = self.user.recipe_set.all().values_list('id', flat=True)
        qs = RecipeIngredient.objects.filter(recipe__id__in=ids)
        self.assertEqual(qs.count(), 1)
