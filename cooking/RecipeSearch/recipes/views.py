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

from .forms import RecipeReviewForm, UserRegisterForm, ProfileForm, UserPantryForm
from .models import Recipe, UserPantry, Ingredient, SavedRecipe

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
        params = {
            'query': query,
            'apiKey': settings.SPOONACULAR_API_KEY,
            'number': 10
        }
        response = requests.get(settings.SPOONACULAR_SEARCH_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            for item in data.get('results', []):
                recipe, created = Recipe.objects.get_or_create(
                    spoonacular_id=item['id'],
                    defaults={
                        'title': item['title'],
                        'image': item.get('image', '')
                    }
                )
                recipes.append(recipe)
        else:
            messages.error(request, "Error fetching recipes. Please try again later.")
    return render(request, 'recipes/recipe_list.html', {
        'recipes': recipes,
        'query': query,
        'current_page': 'recipe_search'
    })

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, spoonacular_id=recipe_id)
    if not recipe.instructions:
        url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
        params = {'apiKey': settings.SPOONACULAR_API_KEY}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            recipe.instructions = data.get('instructions', '')
            recipe.save()
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
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('recipes:profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'users/profile.html', {'form': form, 'current_page': 'profile'})

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
            ingredient, created = Ingredient.objects.get_or_create(name=ingredient_name)
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

@login_required
def add_review(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.method == 'POST':
        form = RecipeReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.recipe = recipe
            review.save()
    return redirect('recipe_detail', recipe_id=recipe_id)
