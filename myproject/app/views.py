from django.shortcuts import render
from django.db.models import Q
from .models import Recipe

def get_recipes(query=None, prep_time=None, cook_time=None, ingredient=None):
    recipes = Recipe.objects.all()

    if query:
        recipes = recipes.filter(
            Q(title__icontains=query) |
            Q(instructions__icontains=query) |
            Q(category__name__icontains=query) |
            Q(cuisine__name__icontains=query)
        )

    if prep_time:
        try:
            prep_time = int(prep_time)
            recipes = recipes.filter(prep_time__lte=prep_time)
        except (ValueError, TypeError):
            pass  # Ignora si prep_time no es un número válido

    if cook_time:
        try:
            cook_time = int(cook_time)
            recipes = recipes.filter(cook_time__lte=cook_time)
        except (ValueError, TypeError):
            pass  # Ignora si cook_time no es un número válido

    if ingredient:
        recipes = recipes.filter(ingredients__name__icontains=ingredient)

    return recipes.select_related('category', 'cuisine').prefetch_related('ingredients')

def home(request):
    query = request.GET.get('q')
    prep_time = request.GET.get('prep_time')
    cook_time = request.GET.get('cook_time')
    ingredient = request.GET.get('ingredient')

    try:
        recipes = get_recipes(query, prep_time, cook_time, ingredient)
        if not recipes and query:
            message = f"No se encontraron recetas para '{query}'."
        else:
            message = ""
    except Exception as e:
        recipes = []
        message = f"Se produjo un error: {e}"

    return render(request, 'app/home.html', {'recipes': recipes, 'message': message})