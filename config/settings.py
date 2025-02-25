INSTALLED_APPS = [
    'app.apps.AppConfig',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'recipe_db',
        'USER': 'recipe_user',
        'PASSWORD': 'recipe_pass',
        'HOST': 'db',
        'PORT': 5432,
    }
}