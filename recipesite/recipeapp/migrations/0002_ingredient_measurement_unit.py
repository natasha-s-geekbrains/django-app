# Generated by Django 5.1.3 on 2024-11-26 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipeapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='measurement_unit',
            field=models.CharField(default='units', max_length=20),
        ),
    ]