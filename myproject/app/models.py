from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre", unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

class Cuisine(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre", unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Cocina"
        verbose_name_plural = "Cocinas"

class Ingredient(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre", unique=True)
    description = models.TextField(blank=True, null=True, verbose_name="Descripción")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Ingrediente"
        verbose_name_plural = "Ingredientes"

class Recipe(models.Model):
    title = models.CharField(max_length=200, verbose_name="Título")
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, verbose_name="Categoría", related_name="recipes"
    )
    cuisine = models.ForeignKey(
        Cuisine, on_delete=models.PROTECT, verbose_name="Cocina", related_name="recipes"
    )
    prep_time = models.PositiveIntegerField(
        verbose_name="Tiempo de preparación (minutos)", validators=[MinValueValidator(0)]
    )
    cook_time = models.PositiveIntegerField(
        verbose_name="Tiempo de cocción (minutos)", validators=[MinValueValidator(0)]
    )
    instructions = models.TextField(verbose_name="Instrucciones")
    image = models.ImageField(upload_to='recipes/', blank=True, null=True, verbose_name="Imagen")
    ingredients = models.ManyToManyField(
        Ingredient, through='RecipeIngredient', verbose_name="Ingredientes", related_name="recipes"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Receta"
        verbose_name_plural = "Recetas"

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name="Receta", related_name="recipe_ingredients"
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, verbose_name="Ingrediente", related_name="recipe_ingredients"
    )
    quantity = models.CharField(max_length=50, verbose_name="Cantidad")

    def __str__(self):
        return f"{self.quantity} de {self.ingredient.name} en {self.recipe.title}"

    class Meta:
        verbose_name = "Ingrediente de Receta"
        verbose_name_plural = "Ingredientes de Recetas"
        constraints = [
            models.UniqueConstraint(fields=['recipe', 'ingredient'], name='unique_recipe_ingredient')
        ]

class UserPantry(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="Usuario", related_name="pantry"
    )
    ingredients = models.ManyToManyField(
        Ingredient, through='UserPantryIngredient', verbose_name="Ingredientes", related_name="pantries"
    )

    def __str__(self):
        return f"Despensa de {self.user.get_username()}"

    class Meta:
        verbose_name = "Despensa de Usuario"
        verbose_name_plural = "Despensas de Usuarios"

class UserPantryIngredient(models.Model):
    pantry = models.ForeignKey(
        UserPantry, on_delete=models.CASCADE, verbose_name="Despensa", related_name="pantry_ingredients"
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, verbose_name="Ingrediente", related_name="pantry_ingredients"
    )
    quantity = models.CharField(max_length=50, verbose_name="Cantidad")

    def __str__(self):
        return f"{self.quantity} de {self.ingredient.name} en la despensa de {self.pantry.user.get_username()}"

    class Meta:
        verbose_name = "Ingrediente de Despensa"
        verbose_name_plural = "Ingredientes de Despensas"
        constraints = [
            models.UniqueConstraint(fields=['pantry', 'ingredient'], name='unique_pantry_ingredient')
        ]
