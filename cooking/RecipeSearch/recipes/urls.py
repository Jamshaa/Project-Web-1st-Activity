from django.urls import path
from . import views


app_name = 'recipes'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('search/', views.recipe_search, name='recipe_search'),
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('profile/', views.profile, name='profile'),
    path('update-bio/', views.update_bio, name='update_bio'),
    path('pantry/', views.pantry, name='pantry'),
    path('add-ingredient/', views.add_pantry_item, name='add_pantry_item'),
    path('remove-ingredient/<int:item_id>/', views.remove_pantry_item, name='remove_pantry_item'),
    path('recipe/<int:recipe_id>/save/', views.save_recipe, name='save_recipe'),
    path('recipe/<int:recipe_id>/remove/', views.remove_saved_recipe, name='remove_saved_recipe'),
    path('saved-recipes/', views.saved_recipes, name='saved_recipes'),  # Nueva ruta
    path('recommendations/', views.recommend_recipes, name='recommendations'),
]
