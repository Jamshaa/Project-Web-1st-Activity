from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)  # Category name
    description = models.TextField(blank=True)           # Optional description

    def __str__(self):
        return self.name
class Recipe(models.Model):
    spoonacular_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=100)
    image = models.URLField(blank=True)
    instructions = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    def __str__(self):
        return f'{self.user.username} Profile'
