image.pngfrom django.core.management.base import BaseCommand
from django.conf import settings
from recipes.models import Recipe, Ingredient, RecipeIngredient
import requests
import time
#test 
class Command(BaseCommand):
    help = 'Updates ingredients for all recipes in the database'

    def handle(self, *args, **options):
        recipes = Recipe.objects.all()
        total = recipes.count()
    
        self.stdout.write(f'Updating ingredients for {total} recipes...')
        
        for index, recipe in enumerate(recipes, 1):
            self.stdout.write(f'Processing recipe {index}/{total}: {recipe.title}')
            
            # Get recipe details from Spoonacular
            url = f"https://api.spoonacular.com/recipes/{recipe.spoonacular_id}/information"
            params = {'apiKey': settings.SPOONACULAR_API_KEY}
            
            try:
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    recipe_data = response.json()
                    
                    # Clear existing ingredients
                    RecipeIngredient.objects.filter(recipe=recipe).delete()
                    
                    # Add new ingredients
                    if 'extendedIngredients' in recipe_data:
                        for ing_data in recipe_data['extendedIngredients']:
                            ing_name = ing_data['name'].lower().strip()
                            
                            ingredient, _ = Ingredient.objects.get_or_create(
                                name=ing_name,
                                defaults={'description': ing_data.get('original', '')}
                            )
                            
                            RecipeIngredient.objects.create(
                                recipe=recipe,
                                ingredient=ingredient,
                                amount=str(ing_data.get('amount', '')),
                                unit=ing_data.get('unit', '')
                            )
                    
                    self.stdout.write(self.style.SUCCESS(f'Successfully updated ingredients for {recipe.title}'))
                else:
                    self.stdout.write(self.style.ERROR(f'Failed to fetch data for {recipe.title}'))
                
                # Sleep to respect API rate limits
                time.sleep(1)
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error processing {recipe.title}: {str(e)}'))
        
        self.stdout.write(self.style.SUCCESS('Successfully updated all recipes')) 