from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)  # Category name
    description = models.TextField(blank=True)           # Optional description

    def __str__(self):
        return self.name

class Recipe(models.Model):
    spoonacular_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=100)
    image = models.URLField(blank=True)
    instructions = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    ingredients = models.ManyToManyField('Ingredient', through='RecipeIngredient')

    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', default='profile_photos/default.jpg')

    def __str__(self):
        return f"{self.user.username} Profile"

class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class UserPantry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    expiration_date = models.DateField(null=True, blank=True)
    image_url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s pantry item: {self.ingredient.name}"

class SavedRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_recipes')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'recipe')

    def __str__(self):
        return f"{self.user.username} saved {self.recipe.title}"

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.CharField(max_length=100, blank=True)
    unit = models.CharField(max_length=50, blank=True)

    class Meta:
        unique_together = ('recipe', 'ingredient')

    def __str__(self):
        return f"{self.amount} {self.unit} {self.ingredient.name} for {self.recipe.title}"

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} on {self.recipe.title}"