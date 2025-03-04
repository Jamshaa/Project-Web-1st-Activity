from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='recipes/login.html'), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('search/', views.recipe_search, name='recipe_search'),
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('profile/', views.profile, name='profile'),
    path('autocomplete/', views.recipe_autocomplete, name='autocomplete'),
]