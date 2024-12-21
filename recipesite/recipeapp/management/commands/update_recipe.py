from django.core.management import BaseCommand

from recipeapp.models import Recipe, Ingredient


class Command(BaseCommand):
    def handle(self, *args, **options):
        recipe = Recipe.objects.first()
        if not recipe:
            self.stdout.write('No order found')
            return
        ingredients = Ingredient.objects.all()

        for ingredient in ingredients:
            recipe.ingredients.add(ingredient)

        recipe.save()

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully added ingredients {recipe.ingredients.all()} to recipe {recipe}'
            )
        )
