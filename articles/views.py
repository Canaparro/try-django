from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import Http404
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
        return redirect('articles:detail', slug=article.slug)

    return render(request, "articles/create.html", context=context)


def article_search_view(request):
    query: str = request.GET.get('q')
    if query is not None:
        qs = Article.objects.search(query)
    else:
        qs = Article.objects.all()
    context = {"articles": qs}
    return render(request, "articles/search.html", context=context)


def article_detail_view(request, slug: str = None):
    article = None
    try:
        article = Article.objects.get(slug=slug)
    except Article.MultipleObjectsReturned:
        article = Article.objects.filter(slug=slug).first()
    except Article.DoesNotExist:
        raise Http404
    except:
        raise Http404

    context = {
        "article": article
    }

    return render(request, "articles/detail.html", context=context)
