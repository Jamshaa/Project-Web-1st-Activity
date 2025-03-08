from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, ProfileForm, UserPantryForm
from .models import Recipe, UserPantry, Ingredient
import requests
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.files.storage import FileSystemStorage

def home(request):
    """Página principal con formulario de búsqueda"""
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
    return render(request, 'recipes/login.html', {'current_page': 'login'})

def recipe_search(request):
    """Vista para buscar recetas utilizando la API de Spoonacular"""
    query = request.GET.get('query')
    recipes = []
    if query:
        params = {
            'query': query,
            'apiKey': settings.SPOONACULAR_API_KEY,
            'number': 10 #number of recipes to show
        }
        response = requests.get(settings.SPOONACULAR_SEARCH_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            for item in data.get('results', []):
                recipe, created = Recipe.objects.get_or_create(
                    spoonacular_id=item['id'],
                    defaults={
                        'title': item['title'],
                        'image': item['image']
                    }
                )
                recipes.append(recipe)
        else:
            messages.error(request, "Error fetching recipes. Please try again later.")
    return render(request, 'recipes/recipe_list.html', {'recipes': recipes, 'query': query, 'current_page': 'recipe_search'})

def recipe_detail(request, recipe_id):
    """Vista para mostrar el detalle de una receta."""
    recipe = get_object_or_404(Recipe, spoonacular_id=recipe_id)
    if not recipe.instructions:
        url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
        params = {
            'apiKey': settings.SPOONACULAR_API_KEY,
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            recipe.instructions = data.get('instructions', '')
            recipe.save()
        else:
            messages.error(request, "Error fetching recipe details.")
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe, 'current_page': 'recipe_detail'})

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
    return render(request, 'recipes/pantry.html', {'pantry_items': pantry_items, 'current_page': 'pantry'})

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
