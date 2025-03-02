from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from app import api_views

router = DefaultRouter()
router.register(r'categories', api_views.CategoryViewSet)
router.register(r'cuisines', api_views.CuisineViewSet)
router.register(r'ingredients', api_views.IngredientViewSet)
router.register(r'recipes', api_views.RecipeViewSet)
router.register(r'recipe-ingredients', api_views.RecipeIngredientViewSet)
router.register(r'user-pantries', api_views.UserPantryViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', include('app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)