# Generated by Django 5.1.6 on 2025-02-28 16:57

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Nombre')),
            ],
            options={
                'verbose_name': 'Categoría',
                'verbose_name_plural': 'Categorías',
            },
        ),
        migrations.CreateModel(
            name='Cuisine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Nombre')),
            ],
            options={
                'verbose_name': 'Cocina',
                'verbose_name_plural': 'Cocinas',
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Nombre')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Descripción')),
            ],
            options={
                'verbose_name': 'Ingrediente',
                'verbose_name_plural': 'Ingredientes',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Título')),
                ('prep_time', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Tiempo de preparación (minutos)')),
                ('cook_time', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Tiempo de cocción (minutos)')),
                ('instructions', models.TextField(verbose_name='Instrucciones')),
                ('image', models.ImageField(blank=True, null=True, upload_to='recipes/', verbose_name='Imagen')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='recipes', to='app.category', verbose_name='Categoría')),
                ('cuisine', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='recipes', to='app.cuisine', verbose_name='Cocina')),
            ],
            options={
                'verbose_name': 'Receta',
                'verbose_name_plural': 'Recetas',
            },
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.CharField(max_length=50, verbose_name='Cantidad')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_ingredients', to='app.ingredient', verbose_name='Ingrediente')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_ingredients', to='app.recipe', verbose_name='Receta')),
            ],
            options={
                'verbose_name': 'Ingrediente de Receta',
                'verbose_name_plural': 'Ingredientes de Recetas',
            },
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(related_name='recipes', through='app.RecipeIngredient', to='app.ingredient', verbose_name='Ingredientes'),
        ),
        migrations.CreateModel(
            name='UserPantry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='pantry', to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Despensa de Usuario',
                'verbose_name_plural': 'Despensas de Usuarios',
            },
        ),
        migrations.CreateModel(
            name='UserPantryIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.CharField(max_length=50, verbose_name='Cantidad')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pantry_ingredients', to='app.ingredient', verbose_name='Ingrediente')),
                ('pantry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pantry_ingredients', to='app.userpantry', verbose_name='Despensa')),
            ],
            options={
                'verbose_name': 'Ingrediente de Despensa',
                'verbose_name_plural': 'Ingredientes de Despensas',
            },
        ),
        migrations.AddField(
            model_name='userpantry',
            name='ingredients',
            field=models.ManyToManyField(related_name='pantries', through='app.UserPantryIngredient', to='app.ingredient', verbose_name='Ingredientes'),
        ),
        migrations.AddConstraint(
            model_name='recipeingredient',
            constraint=models.UniqueConstraint(fields=('recipe', 'ingredient'), name='unique_recipe_ingredient'),
        ),
        migrations.AddConstraint(
            model_name='userpantryingredient',
            constraint=models.UniqueConstraint(fields=('pantry', 'ingredient'), name='unique_pantry_ingredient'),
        ),
    ]
