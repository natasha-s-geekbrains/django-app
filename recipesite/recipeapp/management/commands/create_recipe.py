from typing import Sequence

from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.db import transaction

from recipeapp.models import Recipe, Ingredient


class Command(BaseCommand):
    @transaction.atomic()
    def handle(self, *args, **options):
        self.stdout.write('Create recipe with ingredients')
        user = User.objects.get(username='admin')
        ingredients: Sequence[Ingredient] = Ingredient.objects.all()
        recipe, created = Recipe.objects.get_or_create(
            name='GeneralMix Dried',
            description='A mixture of all the chopped ingredients, pan fried',
            author=user,
            cooking_time_min=9,
        )
        for ingredient in ingredients:
            recipe.ingredients.add(ingredient)
            recipe.save()
        self.stdout.write(f'Created recipe {recipe}')


