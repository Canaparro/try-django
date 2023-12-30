from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Article
from .forms import ArticleForm

# Create your views here.


@login_required
def article_create_view(request):
    form = ArticleForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        article = form.save()
        context['article'] = article

    return render(request, "articles/create.html", context=context)


def article_search_view(request):
    params: dict = request.GET
    query = params.get('q')
    article = None
    try:
        query = int(query)
    except:
        query = None
    if query is not None:
        article = Article.objects.get(id=query)
    context = {"article": article}
    return render(request, "articles/search.html", context=context)


def article_detail_view(request, id: int = None):
    article = Article.objects.get(id=id) if id else None

    context = {
        "article": article
    }

    return render(request, "articles/detail.html", context=context)
