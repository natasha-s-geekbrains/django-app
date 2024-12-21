# Generated by Django 5.1.3 on 2024-12-16 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipeapp', '0011_rename_product_ingredientimage_ingredient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='description',
            field=models.TextField(blank=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(db_index=True, max_length=100),
        ),
    ]