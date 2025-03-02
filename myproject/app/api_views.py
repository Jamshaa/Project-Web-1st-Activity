from rest_framework import viewsets
from .models import UserPantry, RecipeIngredient, Recipe, Ingredient, Cuisine, Category
from .serializers import (
    UserPantrySerializer,
    RecipeIngredientSerializer,
    RecipeSerializer,
    IngredientSerializer,
    CuisineSerializer,
    CategorySerializer
)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CuisineViewSet(viewsets.ModelViewSet):
    queryset = Cuisine.objects.all()
    serializer_class = CuisineSerializer

class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

class RecipeIngredientViewSet(viewsets.ModelViewSet):
    queryset = RecipeIngredient.objects.all()
    serializer_class = RecipeIngredientSerializer

class UserPantryViewSet(viewsets.ModelViewSet):
    queryset = UserPantry.objects.all()
    serializer_class = UserPantrySerializer