from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from .models import Ingredient, Recipe, IngredientImage


# Register your models here.

class RecipeInLine(admin.TabularInline):
    model = Ingredient.recipes.through


class IngredientInline(admin.StackedInline):
    model = IngredientImage


@admin.action(description='Archive ingredients')
def mark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)


@admin.action(description='Unarchive ingredients')
def mark_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=False)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    actions = [
        mark_archived,
        mark_unarchived,
    ]
    inlines = [
        RecipeInLine,
        IngredientInline,
    ]
    list_display = 'pk', 'name', 'description_short', 'measurement_unit', 'archived'
    list_display_links = 'pk', 'name'
    ordering = '-name', 'pk'
    search_fields = 'name', 'description'
    fieldsets = [
        (None, {
            'fields': ('name', 'description'),
        }),
        ('Additional information', {
            'fields': ('measurement_unit',),
            'classes': ('wide', 'collapse',),
        }),
        ('Images', {
            'fields': ('preview',),
        }),
        ('Extra options', {
            'fields': ('archived',),
            'classes': ('collapse',),
            'description': 'Extra options. Field "archived" is for soft deleting.',
        })
    ]

    def description_short(self, obj: Ingredient) -> str:
        if len(obj.description) < 48:
            return obj.description
        return obj.description[:48] + '...'


# class IngredientInLine(admin.TabularInline):
class IngredientInLine(admin.StackedInline):
    model = Recipe.ingredients.through


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [
        IngredientInLine,
    ]
    list_display = 'pk', 'name', 'description_short', 'created_at', 'author_verbose', 'cooking_time_min'
    list_display_links = 'pk', 'name'

    def get_queryset(self, request):
        return Recipe.objects.select_related('author').prefetch_related('ingredients')

    def author_verbose(self, obj: Recipe) -> str:
        return obj.author.first_name or obj.author.username

    def description_short(self, obj: Recipe) -> str:
        if len(obj.description) < 48:
            return obj.description
        return obj.description[:48] + '...'

# admin.site.register(Ingredient, IngredientAdmin)
# admin.site.register(Recipe, RecipeAdmin)
