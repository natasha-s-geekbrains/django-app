from django.contrib.auth.models import User
from django.db import models


# Create your models here.

def ingredient_preview_directory_path(instance: 'Ingredient', filename: str) -> str:
    return 'ingredients/ingredient_{pk}/preview/{filename}'.format(
        pk=instance.pk,
        filename=filename,
    )


class Ingredient(models.Model):
    """
    Модель Ingredient представляет продукт,
    который можно включать в состав рецептов.

    Рецепты тут: :model:`recipeapp.Recipe`
    """
    class Meta:
        ordering = ["name", 'measurement_unit']
        # verbose_name = _('Ingredient')

    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField(null=False, blank=True, db_index=True)
    measurement_unit = models.CharField(max_length=20, default='units')
    archived = models.BooleanField(default=False)
    preview = models.ImageField(null=True, blank=True, upload_to=ingredient_preview_directory_path)

    def __str__(self) -> str:
        return self.name


def ingredient_images_directory_path(instance: 'IngredientImage', filename: str) -> str:
    return 'ingredients/ingredient_{pk}/images/{filename}'.format(
        pk=instance.ingredient.pk,
        filename=filename,
    )


class IngredientImage(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=ingredient_images_directory_path)
    description = models.CharField(max_length=200, null=False, blank=True)


def recipe_preview_directory_path(instance: 'Recipe', filename: str) -> str:
    return 'recipes/recipe_{pk}/preview/{filename}'.format(
        pk=instance.pk,
        filename=filename,
    )


class Recipe(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    cooking_time_min = models.PositiveIntegerField(default=0)
    ingredients = models.ManyToManyField(Ingredient, related_name='recipes')
    preview = models.ImageField(null=True, blank=True, upload_to=recipe_preview_directory_path)


def recipe_images_directory_path(instance: 'RecipeImage', filename: str) -> str:
    return 'recipes/recipe_{pk}/images/{filename}'.format(
        pk=instance.recipe.pk,
        filename=filename,
    )


class RecipeImage(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=recipe_images_directory_path)
    description = models.CharField(max_length=200, null=False, blank=True)
