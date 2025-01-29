from django import forms
from django.core import validators
from django.forms import ModelForm

from .models import Recipe, Ingredient


class RecipeForm(forms.ModelForm):

    ingredients = forms.ModelMultipleChoiceField(
        label='Ингредиенты:',
        queryset=Ingredient.objects.all(),
        widget=forms.CheckboxSelectMultiple())

    name = forms.CharField(
        label='Название ингредиента:',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    description = forms.CharField(
        label='Как приготовить:',
        widget=forms.Textarea(
            attrs={'class': 'form-control'}
        )
    )

    cooking_time_min = forms.IntegerField(
        label='Время приготовления (мин):',
        initial=0,
        widget=forms.NumberInput(
            attrs={'class': 'form-control'}
        )
    )

    preview = forms.ImageField(
        label='Изображение:',
        widget=forms.FileInput(
            attrs={'class': 'form-control'}
        )
    )

    class Meta:
        model = Recipe
        fields = 'name', 'description', 'cooking_time_min', 'ingredients', 'preview'


class IngredientForm(forms.ModelForm):
    name = forms.CharField(
        label='Название ингредиента:',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    description = forms.CharField(
        label='Примечание:',
        widget=forms.Textarea(
            attrs={'class': 'form-control'}
        )
    )

    measurement_unit = forms.CharField(
        label='Единица измерения:',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    preview = forms.ImageField(
        label='Изображение:',
        widget=forms.FileInput(
            attrs={'class': 'form-control'}
        )
    )

    class Meta:
        model = Ingredient
        fields = 'name', 'description', 'measurement_unit', 'preview'


