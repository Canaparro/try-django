from django.shortcuts import get_object_or_404, redirect, render
from django.forms.models import modelformset_factory
from django.contrib.auth.decorators import login_required

from recipes.forms import RecipeForm, RecipeIngredientForm
from .models import Recipe, RecipeIngredient

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
    recipe_ingredient_form_set_factory = modelformset_factory(
        RecipeIngredient, form=RecipeIngredientForm, extra=0)
    qs = obj.recipeingredient_set.all()
    form_set = recipe_ingredient_form_set_factory(
        request.POST or None, queryset=qs)
    context = {
        "form": form,
        "form_set": form_set,
        "object": obj
    }
    if form.is_valid() and form_set.is_valid():
        parent = form.save()
        for ingredient_form in form_set:
            child = ingredient_form.save(commit=False)
            if child.recipe is None:
                child.recipe = parent
            child.save()
        context['message'] = 'Data saved.'
    return render(request, "recipes/create-update.html", context=context)
