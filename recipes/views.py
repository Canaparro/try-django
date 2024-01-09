from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from recipes.forms import RecipeForm
from .models import Recipe

# Create your views here.


@login_required
def recipe_list_view(request):
    qs = Recipe.objects.filter(user=request.user)
    context = {
        "object_list": qs
    }
    return render(request, "recipes/list.html", context=context)


@login_required
def recipe_detail_view(request, id=None):
    obj = get_object_or_404(Recipe, id=id, user=request.user)
    context = {
        "recipe": obj
    }
    return render(request, "recipes/detail.html", context=context)


@login_required
def recipe_create_view(request):
    form = RecipeForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        return redirect(obj.get_absolute_url())
    context = {
        'form': form
    }
    return render(request, "recipes/create-update.html", context)


@login_required
def recipe_update_view(request, id=None):
    obj = get_object_or_404(Recipe, id=id, user=request.user)
    form = RecipeForm(request.POST or None, instance=obj)
    context = {
        "form": form,
        "object": obj
    }
    if form.is_valid():
        obj.save()
        context['message'] = 'Data saved.'
    return render(request, "recipes/create-update.html", context=context)
