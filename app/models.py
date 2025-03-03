from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Cuisine(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    cuisine = models.ForeignKey(Cuisine, on_delete=models.PROTECT)
    prep_time = models.PositiveIntegerField()
    cook_time = models.PositiveIntegerField()
    instructions = models.TextField()
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')

    def __str__(self):
        return self.title

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.quantity} de {self.ingredient.name}"

class UserPantry(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='pantry')
    ingredients = models.ManyToManyField(Ingredient, through='UserPantryIngredient')

    def __str__(self):
        return f"Despensa de {self.user.username}"

class UserPantryIngredient(models.Model):
    pantry = models.ForeignKey(UserPantry, on_delete=models.CASCADE, related_name='pantry_ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.quantity} de {self.ingredient.name}"