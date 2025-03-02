from django.contrib import admin
from .models import Category, Cuisine, Recipe

admin.site.register(Category)
admin.site.register(Cuisine)
admin.site.register(Recipe)