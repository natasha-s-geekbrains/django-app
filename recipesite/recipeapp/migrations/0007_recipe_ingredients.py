# Generated by Django 5.1.3 on 2024-11-27 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipeapp', '0006_recipe_cooking_time_min'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(related_name='recipes', to='recipeapp.ingredient'),
        ),
    ]
