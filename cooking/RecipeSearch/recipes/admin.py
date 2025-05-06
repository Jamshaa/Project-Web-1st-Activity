from django.contrib import admin
from .models import Profile, Recipe, Ingredient, UserPantry, Category, Cuisine

class UserPantryAdmin(admin.ModelAdmin):
    list_display = ('user', 'ingredient', 'expiration_date', 'image_url')

admin.site.register(Profile)
admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(UserPantry, UserPantryAdmin)
admin.site.register(Category)
admin.site.register(Cuisine)


