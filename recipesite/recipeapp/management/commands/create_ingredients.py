from django.core.management import BaseCommand

from recipeapp.models import Ingredient


class Command(BaseCommand):
    """
    Creates ingredients
    """

    def handle(self, *args, **options):
        self.stdout.write('Create ingredients')

        ingredients_names = [
            'Milk',
            'Salt',
            'Olive oil',
        ]
        for ingredient_name in ingredients_names:
            ingredient, created = Ingredient.objects.get_or_create(name=ingredient_name)
            self.stdout.write(f'Created ingredient {ingredient.name}')

        self.stdout.write(self.style.SUCCESS('Ingredients created'))
