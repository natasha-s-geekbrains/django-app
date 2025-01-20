from django import forms
from django.core import validators
from django.forms import ModelForm

from .models import Recipe, Ingredient


class RecipeForm(forms.ModelForm):
    ingredients = forms.ModelMultipleChoiceField(queryset=Ingredient.objects.all(), widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = Recipe
        fields = 'name', 'description', 'cooking_time_min', 'ingredients', 'preview'


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = 'name', 'description', 'measurement_unit', 'preview'

    images = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'allow_multiple_selected': True}),
    )
