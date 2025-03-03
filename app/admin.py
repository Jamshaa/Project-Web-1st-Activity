from django.contrib import admin
from .models import *

admin.site.register(Category)
admin.site.register(Cuisine)
admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(RecipeIngredient)
admin.site.register(UserPantry)
admin.site.register(UserPantryIngredient)