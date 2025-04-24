from django.core.management.base import BaseCommand
from recipes.models import Recipe, Ingredient, RecipeIngredient

class Command(BaseCommand):
    help = 'Adds initial recipes with ingredients'

    def handle(self, *args, **options):
        # Create some basic recipes
        recipes_data = [
            {
                'title': 'Simple Garlic Chicken',
                'spoonacular_id': 1001,
                'ingredients': ['chicken', 'garlic', 'salt', 'onion'],
                'instructions': 'Season chicken with salt. Cook with garlic and onions until done.'
            },
            {
                'title': 'Basic Fried Rice',
                'spoonacular_id': 1002,
                'ingredients': ['rice', 'egg', 'onion', 'garlic', 'salt', 'soy sauce', 'vegetable oil'],
                'instructions': 'Cook rice. Fry with eggs, onions, and garlic. Season with soy sauce and salt.'
            },
            {
                'title': 'Tomato & Garlic Chicken',
                'spoonacular_id': 1003,
                'ingredients': ['chicken', 'tomato', 'garlic', 'onion', 'salt'],
                'instructions': 'Cook chicken with garlic and onions. Add tomatoes and simmer. Season with salt.'
            }
        ]

        for recipe_data in recipes_data:
            # Create or update recipe
            recipe, _ = Recipe.objects.get_or_create(
                spoonacular_id=recipe_data['spoonacular_id'],
                defaults={
                    'title': recipe_data['title'],
                    'instructions': recipe_data['instructions']
                }
            )

            # Add ingredients
            for ing_name in recipe_data['ingredients']:
                # Standardize ingredient name
                ing_name = ing_name.lower().strip()
                if ing_name.endswith('s'):
                    ing_name = ing_name[:-1]

                # Create or get ingredient
                ingredient, _ = Ingredient.objects.get_or_create(
                    name=ing_name,
                    defaults={'description': ''}
                )

                # Create recipe-ingredient relationship
                RecipeIngredient.objects.get_or_create(
                    recipe=recipe,
                    ingredient=ingredient
                )

            self.stdout.write(self.style.SUCCESS(f'Successfully added recipe: {recipe.title}')) 