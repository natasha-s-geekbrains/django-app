from django import forms
from django.core import validators
from django.forms import ModelForm

from .models import Recipe, Ingredient


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = 'name', 'description', 'cooking_time_min', 'ingredients'


# class RecipeForm(forms.Form):
#     name = forms.CharField(max_length=100)
#     description = forms.CharField(label='Description (Cooking steps)',
#                                   widget=forms.Textarea(attrs={'rows': '15', 'cols': '45'}))
#     cooking_time_min = forms.DecimalField(min_value=0.01, decimal_places=2)


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = 'name', 'description', 'measurement_unit', 'preview'

    images = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'allow_multiple_selected': True}),
    )
