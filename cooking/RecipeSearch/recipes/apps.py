from django.apps import AppConfig


class RecipesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recipes'
class RecipesConfig(AppConfig):
    name = 'recipes'

    def ready(self):
        from recipes import signals  