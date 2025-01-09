from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    RecipeIndexView,
    RecipesListView,
    RecipeDetailView,
    IngredientDetailsView,
    IngredientsListView,
    IngredientCreateView,
    IngredientUpdateView,
    IngredientDeleteView,
    IngredientViewSet,
    RecipeCreateView,
    RecipeUpdateView,
    RecipeDeleteView,
)

app_name = 'recipeapp'

routers = DefaultRouter()
routers.register('ingredients', IngredientViewSet)

urlpatterns = [
    path('', RecipeIndexView.as_view(), name='index'),
    path('api/', include(routers.urls)),
    path('ingred/', IngredientsListView.as_view(), name='ingredients_list'),
    path('ingred/create/', IngredientCreateView.as_view(), name='ingredient_create'),
    path('ingred/<int:pk>/', IngredientDetailsView.as_view(), name='ingredient_details'),
    path('ingred/<int:pk>/update', IngredientUpdateView.as_view(), name='ingredient_update'),
    path('ingred/<int:pk>/archive', IngredientDeleteView.as_view(), name='ingredient_delete'),
    path('recipes/', RecipesListView.as_view(), name='recipes_list'),
    path('recipes/<int:pk>/', RecipeDetailView.as_view(), name='recipe_details'),
    path('recipes/create/', RecipeCreateView.as_view(), name='recipe_create'),
    path('recipes/<int:pk>/update', RecipeUpdateView.as_view(), name='recipe_update'),
    path('recipes/<int:pk>/archive', RecipeDeleteView.as_view(), name='recipe_delete'),
]
