from django.db import models
from django.contrib.auth.models import User

class Recipe(models.Model):
    title = models.CharField(max_length=255)
    spoonacular_id = models.IntegerField(unique=True)
    image = models.URLField()
    instructions = models.TextField()

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_recipes = models.ManyToManyField(Recipe, blank=True)

    def __str__(self):
        return self.user.username
