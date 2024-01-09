from django import forms

from .models import Recipe, RecipeIngredient


class RecipeForm(forms.ModelForm):
    required_css_class = 'required-field'
    name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Recipe name'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))

    class Meta:
        model = Recipe
        fields = ['name', 'description', 'directions']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        config = {
            'class': 'form-control'
        }
        for field in self.fields:
            config['placeholder'] = f'Recipe {field}'
            self.fields[field].widget.attrs.update(config)


class RecipeIngredientForm(forms.ModelForm):

    class Meta:
        model = RecipeIngredient
        fields = ['name', 'quantity', 'unit']
