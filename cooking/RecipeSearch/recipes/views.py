from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, ProfileForm
from .models import Recipe
import requests

def home(request):
    """Página principal con formulario de búsqueda"""
    return render(request, 'recipes/home.html')

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
    return render(request, 'recipes/register.html', {'form': form})

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
    return render(request, 'recipes/recipe_list.html', {'recipes': recipes, 'query': query})

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
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})

def recipe_autocomplete(request):
    """Devuelve una lista de sugerencias para autocompletar la búsqueda."""
    term = request.GET.get('term', '')
    suggestions = []
    if term:
        url = "https://api.spoonacular.com/recipes/autocomplete"
        params = {
            'query': term,
            'number': 5,  # Número de sugerencias
            'apiKey': settings.SPOONACULAR_API_KEY,
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            suggestions = response.json()
    return JsonResponse(suggestions, safe=False)

def user_logout(request):
    logout(request)
    return render(request, 'recipes/logout.html')

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

    return render(request, 'users/profile.html', {'form': form})