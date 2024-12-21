"""
В этом модуле лежат различные наборы представлений.

Разные view сайта рецептов: по рецептам, ингредиентам и т.д.
"""
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
import random

from .models import Ingredient, Recipe, IngredientImage
from .forms import RecipeForm, IngredientForm
from .serializers import IngredientSerializer


# Create your views here.


class IngredientViewSet(ModelViewSet):
    """
    Набор представлений для действий над Ingredient.

    Полный CRUD для сущностей продукта.
    """

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter
    ]
    search_fields = ['name', 'description']
    filterset_fields = [
        'name',
        'description',
        'archived',
    ]
    ordering_fields = [
        'name',
        'description',
        'measurement_unit',
        'archived',
    ]


class RecipeIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        recipes = list(Recipe.objects.all())
        recipes = random.sample(recipes, 3)
        context = {
            'recipes': recipes,
            'items': 5,
        }
        return render(request, 'recipeapp/recipe-index.html', context=context)


class IngredientDetailsView(DetailView):
    template_name = 'recipeapp/ingredient-details.html'
    # model = Ingredient
    queryset = Ingredient.objects.prefetch_related('images')
    context_object_name = 'ingredient'


class IngredientsListView(ListView):
    template_name = 'recipeapp/ingredients-list.html'
    context_object_name = 'ingredients'
    queryset = Ingredient.objects.filter(archived=False)


def create_ingredient(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            form.save()
            url = reverse('recipeapp:ingredients_list')
            return redirect(url)
    else:
        form = IngredientForm()

    context = {
        'form': form
    }

    return render(request, 'recipeapp/create-ingredient.html', context=context)


class IngredientCreateView(CreateView):
    model = Ingredient
    fields = 'name', 'description', 'measurement_unit', 'preview'
    success_url = reverse_lazy('recipeapp:ingredients_list')


class IngredientUpdateView(UpdateView):
    model = Ingredient
    # fields = 'name', 'description', 'measurement_unit', 'archived', 'preview'
    template_name_suffix = '_update_form'
    form_class = IngredientForm

    def get_success_url(self):
        return reverse(
            'recipeapp:ingredient_details',
            kwargs={'pk': self.object.pk}
        )

    def form_valid(self, form):
        response = super().form_valid(form)
        for image in form.files.getlist('images'):
            IngredientImage.objects.create(
                ingredient=self.object,
                image=image,
            )

        return response


class IngredientDeleteView(DeleteView):
    model = Ingredient
    success_url = reverse_lazy('recipeapp:ingredients_list')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


def recipes_list(request: HttpRequest):
    context = {
        'recipes': Recipe.objects.select_related('author').prefetch_related('ingredients').all(),
    }
    return render(request, 'recipeapp/recipes-list.html', context=context)


class RecipesListView(LoginRequiredMixin, ListView):
    queryset = (
        Recipe.objects.
        select_related('author').
        prefetch_related('ingredients')
    )


# class RecipeDetailView(PermissionRequiredMixin, DetailView):
class RecipeDetailView(DetailView):
    # permission_required = 'recipeapp.view_recipe'
    queryset = (
        Recipe.objects.
        select_related('author').
        prefetch_related('ingredients')
    )


@login_required
def create_recipe(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            cooking_time_min = form.cleaned_data['cooking_time_min']
            description = form.cleaned_data['description']
            author = request.user
            recipe = Recipe.objects.create(
                name=name,
                description=description,
                cooking_time_min=cooking_time_min,
                author=author
            )
            ingredients = form.cleaned_data['ingredients']
            for ingredient in ingredients:
                recipe.ingredients.add(ingredient)
            recipe.save()
            print("Ингредиенты:", type(ingredients))
            url = reverse('recipeapp:recipes_list')
            return redirect(url)
        else:
            context = {
                'form': form
            }
            return render(request, 'recipeapp/create-recipe.html', context=context)
    else:
        form = RecipeForm()

    context = {
        'form': form
    }

    return render(request, 'recipeapp/create-recipe.html', context=context)
