from django.shortcuts import render

from .models import Article

# Create your views here.

def article_detail_view(request, id: int = None):
    article = Article.objects.get(id=id) if id else None
    
    context = {
        "article": article
    }

    return render(request, "articles/detail.html", context=context)