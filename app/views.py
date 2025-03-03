from rest_framework import viewsets, serializers
from django.shortcuts import render
from .models import Recipe, Category

def home(request):
    query = request.GET.get('q', '')
    prep_time = request.GET.get('prep_time', '')
    cook_time = request.GET.get('cook_time', '')
    ingredient = request.GET.get('ingredient', '')

    recipes = Recipe.objects.all()

    if query:
        recipes = recipes.filter(title__icontains=query)
    if prep_time:
        recipes = recipes.filter(prep_time__lte=prep_time)
    if cook_time:
        recipes = recipes.filter(cook_time__lte=cook_time)
    if ingredient:
        recipes = recipes.filter(recipe_ingredients__ingredient__name__icontains=ingredient)

    return render(request, 'app/home.html', {'recipes': recipes})

# Serializador para Category
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

# Serializador para Recipe
class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'

# Vista para Recipe
class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

# Vista para Category
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
