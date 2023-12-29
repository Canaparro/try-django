from django.shortcuts import render

from .models import Article

# Create your views here.

def article_create_view(request):
    context={}
    if request.method == 'POST':
        body: dict = request.POST
        title = body.get("title")
        content = body.get("content")
        article = Article.objects.create(title=title, content=content)
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
