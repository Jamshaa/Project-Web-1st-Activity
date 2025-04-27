from django.contrib import admin
from .models import Profile, Recipe, Ingredient, UserPantry, RecipeReview

class UserPantryAdmin(admin.ModelAdmin):
    list_display = ('user', 'ingredient', 'expiration_date', 'image_url')

@admin.register(RecipeReview)
class RecipeReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'recipe__title', 'comment')

admin.site.register(Profile)
admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(UserPantry, UserPantryAdmin)


