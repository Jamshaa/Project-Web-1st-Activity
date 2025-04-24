from django.core.management.base import BaseCommand
from django.conf import settings
from recipes.models import Recipe, Ingredient, RecipeIngredient
import requests
import time

class Command(BaseCommand):
    help = 'Updates instructions for all recipes from Spoonacular API'

    def handle(self, *args, **options):
        recipes = Recipe.objects.filter(instructions__isnull=True) | Recipe.objects.filter(instructions='')
        total = recipes.count()
        
        self.stdout.write(f'Found {total} recipes without instructions. Starting update...')
        
        for index, recipe in enumerate(recipes, 1):
            self.stdout.write(f'Processing recipe {index}/{total}: {recipe.title}')
            
            url = f"https://api.spoonacular.com/recipes/{recipe.spoonacular_id}/information"
            params = {'apiKey': settings.SPOONACULAR_API_KEY}
            
            try:
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    recipe.instructions = data.get('instructions', '')
                    recipe.save()
                    
                    # Also update ingredients if they don't exist
                    if 'extendedIngredients' in data and not recipe.recipeingredient_set.exists():
                        for ing_data in data['extendedIngredients']:
                            ingredient, _ = Ingredient.objects.get_or_create(
                                name=ing_data['name'].lower(),
                                defaults={'description': ing_data.get('original', '')}
                            )
                            RecipeIngredient.objects.get_or_create(
                                recipe=recipe,
                                ingredient=ingredient,
                                defaults={
                                    'amount': str(ing_data.get('amount', '')),
                                    'unit': ing_data.get('unit', '')
                                }
                            )
                    
                    self.stdout.write(self.style.SUCCESS(f'Successfully updated {recipe.title}'))
                else:
                    self.stdout.write(self.style.ERROR(f'Failed to fetch data for {recipe.title}'))
                
                # Sleep to respect API rate limits
                time.sleep(1)
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error processing {recipe.title}: {str(e)}'))
        
        self.stdout.write(self.style.SUCCESS('Successfully updated all recipes')) 