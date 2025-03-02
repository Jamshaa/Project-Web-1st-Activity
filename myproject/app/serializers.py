from rest_framework import serializers
from .models import (
    Category, Cuisine, Ingredient, Recipe,
    RecipeIngredient, UserPantry, UserPantryIngredient
)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CuisineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuisine
        fields = '__all__'

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'

class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient_name = serializers.ReadOnlyField(source='ingredient.name')

    class Meta:
        model = RecipeIngredient
        fields = ['id', 'ingredient', 'ingredient_name', 'quantity']

class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(source='recipeingredient_set', many=True, read_only=True)
    category_name = serializers.ReadOnlyField(source='category.name')
    cuisine_name = serializers.ReadOnlyField(source='cuisine.name')

    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'category', 'category_name',
            'cuisine', 'cuisine_name', 'prep_time', 'cook_time',
            'instructions', 'image', 'ingredients'
        ]

class UserPantryIngredientSerializer(serializers.ModelSerializer):
    ingredient_name = serializers.ReadOnlyField(source='ingredient.name')

    class Meta:
        model = UserPantryIngredient
        fields = ['id', 'ingredient', 'ingredient_name', 'quantity']

class UserPantrySerializer(serializers.ModelSerializer):
    ingredients = UserPantryIngredientSerializer(source='userpantryingredient_set', many=True, read_only=True)
    user = serializers.StringRelatedField()  # Muestra el nombre de usuario

    class Meta:
        model = UserPantry
        fields = ['id', 'user', 'ingredients']
