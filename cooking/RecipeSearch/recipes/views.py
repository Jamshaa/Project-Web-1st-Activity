from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
import requests
import json
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Count, Q

from .forms import UserRegisterForm, ProfileForm, UserPantryForm, RecipeForm
from .models import Recipe, UserPantry, Ingredient, SavedRecipe, RecipeIngredient

def home(request):
    return render(request, 'recipes/home.html', {'current_page': 'home'})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('recipes:home')
        else:
            messages.error(request, "Registration failed. Please check the form.")
    else:
        form = UserRegisterForm()
    return render(request, 'recipes/register.html', {'form': form, 'current_page': 'register'})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect('recipes:home')
        else:
            messages.error(request, "Invalid credentials, please try again.")
    return render(request, 'recipes/login.html', {'current_page': 'login'})

def recipe_search(request):
    query = request.GET.get('query')
    recipes = []
    if query:
        # First, search for recipes
        search_params = {
            'query': query,
            'apiKey': settings.SPOONACULAR_API_KEY,
            'number': 10
        }
        search_response = requests.get(settings.SPOONACULAR_SEARCH_URL, params=search_params)
        
        if search_response.status_code == 200:
            search_data = search_response.json()
            
            for item in search_data.get('results', []):
                # Get detailed recipe information including ingredients
                detail_url = f"https://api.spoonacular.com/recipes/{item['id']}/information"
                detail_params = {'apiKey': settings.SPOONACULAR_API_KEY}
                detail_response = requests.get(detail_url, params=detail_params)
                
                if detail_response.status_code == 200:
                    recipe_data = detail_response.json()
                    
                    # Create or update recipe
                    recipe, created = Recipe.objects.get_or_create(
                        spoonacular_id=recipe_data['id'],
                        defaults={
                            'title': recipe_data['title'],
                            'image': recipe_data.get('image', ''),
                            'instructions': recipe_data.get('instructions', '')
                        }
                    )

                    # If recipe exists, update its fields
                    if not created:
                        recipe.title = recipe_data['title']
                        recipe.image = recipe_data.get('image', '')
                        recipe.instructions = recipe_data.get('instructions', '')
                        recipe.save()
                    
                    # Save ingredients
                    if 'extendedIngredients' in recipe_data:
                        # Clear existing ingredients for this recipe
                        RecipeIngredient.objects.filter(recipe=recipe).delete()
                        
                        for ing_data in recipe_data['extendedIngredients']:
                            # Clean ingredient name
                            ing_name = ing_data['name'].lower().strip()
                            
                            # Create or get ingredient
                            ingredient, _ = Ingredient.objects.get_or_create(
                                name=ing_name,
                                defaults={'description': ing_data.get('original', '')}
                            )
                            
                            # Create recipe-ingredient relationship
                            RecipeIngredient.objects.create(
                                recipe=recipe,
                                ingredient=ingredient,
                                amount=str(ing_data.get('amount', '')),
                                unit=ing_data.get('unit', '')
                            )
                    
                    recipes.append(recipe)
                else:
                    messages.error(request, f"Error fetching details for recipe {item['title']}")
        else:
            messages.error(request, "Error fetching recipes. Please try again later.")
    
    return render(request, 'recipes/recipe_list.html', {
        'recipes': recipes,
        'query': query,
        'current_page': 'recipe_search'
    })

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, spoonacular_id=recipe_id)
    if not recipe.instructions or not recipe.recipeingredient_set.exists():
        url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
        params = {'apiKey': settings.SPOONACULAR_API_KEY}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            recipe.instructions = data.get('instructions', '')
            recipe.save()
            
            # Save ingredients if they don't exist
            if 'extendedIngredients' in data:
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
        else:
            messages.error(request, "Error fetching recipe details.")
    return render(request, 'recipes/recipe_detail.html', {
        'recipe': recipe,
        'current_page': 'recipe_detail'
    })

def user_logout(request):
    logout(request)
    return render(request, 'recipes/logout.html', {'current_page': 'logout'})

@login_required
def profile(request):
    profile = request.user.profile 
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            # Update User model fields
            user = request.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('recipes:profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'users/profile.html', {
        'form': form,
        'current_page': 'profile',
        'user': request.user
    })

@csrf_exempt
def update_bio(request):
    if request.method == "POST":
        data = json.loads(request.body)
        request.user.profile.bio = data.get("bio", "")
        request.user.profile.save()
        return JsonResponse({"message": "Bio updated successfully"})
    return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
def pantry(request):
    pantry_items = UserPantry.objects.filter(user=request.user).select_related('ingredient')
    today = timezone.now().date()
    for item in pantry_items:
        if item.expiration_date < today:
            item.status = 'Expired'
        elif item.expiration_date <= today + timedelta(days=3):
            item.status = 'Expiring Soon'
        else:
            item.status = 'Good'
    return render(request, 'recipes/pantry.html', {
        'pantry_items': pantry_items,
        'current_page': 'pantry'
    })

@login_required
def add_pantry_item(request):
    if request.method == 'POST':
        ingredient_name = request.POST.get('ingredient_name')
        expiration_date = request.POST.get('expiration_date')
        image = request.FILES.get('image')
        
        if ingredient_name and expiration_date:
            # Standardize the ingredient name
            ingredient_name = standardize_ingredient_name(ingredient_name.lower().strip())
            
            ingredient, created = Ingredient.objects.get_or_create(
                name=ingredient_name,
                defaults={'description': ''}
            )
            
            # Check if this ingredient is already in the user's pantry
            existing_item = UserPantry.objects.filter(
                user=request.user,
                ingredient=ingredient
            ).first()
            
            if existing_item:
                # Update existing item's expiration date
                existing_item.expiration_date = expiration_date
                if image:
                    fs = FileSystemStorage()
                    filename = fs.save(image.name, image)
                    existing_item.image_url = fs.url(filename)
                existing_item.save()
            else:
                # Create new pantry item
                pantry_item = UserPantry(
                    user=request.user,
                    ingredient=ingredient,
                    expiration_date=expiration_date
                )
                if image:
                    fs = FileSystemStorage()
                    filename = fs.save(image.name, image)
                    pantry_item.image_url = fs.url(filename)
                pantry_item.save()
            
            return redirect('recipes:pantry')
    return redirect('recipes:pantry')

@login_required
def remove_pantry_item(request, item_id):
    if request.method == 'POST':
        UserPantry.objects.filter(id=item_id, user=request.user).delete()
        return JsonResponse({"message": "Item removed successfully"})
    return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
def save_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, spoonacular_id=recipe_id)
    saved, created = SavedRecipe.objects.get_or_create(user=request.user, recipe=recipe)
    message = "Recipe saved successfully." if created else "Recipe was already saved."
    return redirect('recipes:saved_recipes')

@login_required
def remove_saved_recipe(request, recipe_id):
    try:
        saved = SavedRecipe.objects.get(user=request.user, recipe__spoonacular_id=recipe_id)
        saved.delete()
        message = "Saved recipe removed."
    except SavedRecipe.DoesNotExist:
        message = "Recipe not found in your saved list."
    return redirect('recipes:saved_recipes')

@login_required
def saved_recipes(request):
    saved = SavedRecipe.objects.filter(user=request.user).select_related('recipe')
    return render(request, 'recipes/saved_recipes.html', {
        'saved_recipes': saved,
        'current_page': 'saved_recipes'
    })

def update_recipe_instructions(recipe):
    """Fetch and update recipe instructions from Spoonacular API"""
    if not recipe.instructions:
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
                return True
        except Exception as e:
            print(f"Error updating recipe {recipe.title}: {str(e)}")
    return False

@login_required
def recommend_recipes(request):
    from datetime import date
    from django.db.models import Count, F, Q
    
    # Get user's pantry ingredients that haven't expired
    user_pantry_ingredients = UserPantry.objects.filter(
        user=request.user,
        expiration_date__gte=date.today()
    ).select_related('ingredient')

    # Get all recipes from database
    all_recipes = Recipe.objects.all().prefetch_related('recipeingredient_set__ingredient')
    
    # Calculate matches for each recipe
    recommended_recipes = []
    for recipe in all_recipes:
        recipe_ingredients = set(ri.ingredient.name.lower() for ri in recipe.recipeingredient_set.all())
        user_ingredients = set(item.ingredient.name.lower() for item in user_pantry_ingredients)
        
        if recipe_ingredients:  # Only process recipes that have ingredients
            matched_ingredients = recipe_ingredients.intersection(user_ingredients)
            match_percentage = (len(matched_ingredients) / len(recipe_ingredients)) * 100
            
            if match_percentage >= 50:  # Show recipes with at least 50% match
                recipe.match_percentage = match_percentage
                recipe.matched_ingredients = len(matched_ingredients)
                recipe.total_ingredients = len(recipe_ingredients)
                recommended_recipes.append(recipe)
    
    # Sort by match percentage (highest first)
    recommended_recipes.sort(key=lambda x: x.match_percentage, reverse=True)

    return render(request, 'recipes/recommendations.html', {
        'recipes': recommended_recipes,
        'current_page': 'recommendations'
    })

def standardize_ingredient_name(name):
    """Standardize ingredient names by removing plurals and common variations"""
    # Remove trailing 's' if it exists
    if name.endswith('s'):
        name = name[:-1]
    return name

@login_required
def create_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user  # Set the recipe owner
            recipe.save()
            form.save_m2m()  # Save many-to-many relationships
            return redirect('recipes:recipe_detail', recipe_id=recipe.spoonacular_id)
    else:
        form = RecipeForm()
    return render(request, 'recipes/create_recipe.html', {'form': form})
