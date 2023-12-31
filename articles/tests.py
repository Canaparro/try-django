from django.test import TestCase

# Create your tests here.

from .models import Article, slugify_instance_title


class ArticleTestCase(TestCase):

    def setUp(self):
        self.number_of_articles = 50
        for i in range(self.number_of_articles):
            Article(title='hello world', content='something else').save()

    def test_queryset_exists(self):
        qs = Article.objects.all()
        self.assertTrue(qs.exists())

    def test_queryset_count(self):
        qs = Article.objects.all()
        self.assertEqual(qs.count(), self.number_of_articles)

    def test_hello_world_slug(self):
        obj = Article.objects.all().order_by("id").first()
        slug = obj.slug
        self.assertEqual(slug, 'hello-world')

    def test_hello_world_unique_slug(self):
        qs = Article.objects.exclude(slug__iexact='hello-world')
        for obj in qs:
            slug = obj.slug
            self.assertNotEqual(slug, 'hello-world')

    def test_slugify_instante_title(self):
        new_slugs = Article.objects.all().values_list('slug', flat=True)
        unique_slugs = list(set(new_slugs))
        self.assertEqual(len(new_slugs), len(unique_slugs))

    def test_article_search_manager(self):
        qs = Article.objects.search(query='hello world')
        self.assertEqual(qs.count(), self.number_of_articles)
        qs = Article.objects.search(query='something else')
        self.assertEqual(qs.count(), self.number_of_articles)
