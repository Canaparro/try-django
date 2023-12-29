"""
To render html web pages
"""

from django.http import HttpResponse
from articles.models import Article
from django.template.loader import render_to_string

def home_view(request):
    """
    Take in a request
    Return HTML as response
    """
    article_obj = Article.objects.get(id=2)
    article_objs = Article.objects.all()
    context = {
        "article_objs": article_objs,
        "id" : article_obj.id,
        "title" : article_obj.title,
        "content" : article_obj.content
    }

    HTML_STRING = render_to_string("home-view.html", context=context)
    return HttpResponse(HTML_STRING)