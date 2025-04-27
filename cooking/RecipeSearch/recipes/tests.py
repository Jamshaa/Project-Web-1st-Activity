from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Recipe, RecipeReview

# Create your tests here.

class RecipeReviewTests(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create test recipe
        self.recipe = Recipe.objects.create(
            spoonacular_id=12345,
            title='Test Recipe'
        )
        
        # Create client
        self.client = Client()

    def test_create_review(self):
        # Login
        self.client.login(username='testuser', password='testpass123')
        
        # Submit review
        response = self.client.post(
            reverse('add_review', args=[self.recipe.id]),
            {
                'rating': 5,
                'comment': 'Great recipe!'
            }
        )
        
        # Check if review was created
        self.assertEqual(RecipeReview.objects.count(), 1)
        review = RecipeReview.objects.first()
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, 'Great recipe!')
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.recipe, self.recipe)

    def test_duplicate_review(self):
        # Create initial review
        RecipeReview.objects.create(
            user=self.user,
            recipe=self.recipe,
            rating=4,
            comment='First review'
        )
        
        # Login
        self.client.login(username='testuser', password='testpass123')
        
        # Try to submit second review
        response = self.client.post(
            reverse('add_review', args=[self.recipe.id]),
            {
                'rating': 5,
                'comment': 'Second review'
            }
        )
        
        # Check that only one review exists
        self.assertEqual(RecipeReview.objects.count(), 1)
        review = RecipeReview.objects.first()
        self.assertEqual(review.comment, 'First review')

    def test_unauthenticated_user(self):
        # Try to submit review without logging in
        response = self.client.post(
            reverse('add_review', args=[self.recipe.id]),
            {
                'rating': 5,
                'comment': 'Great recipe!'
            }
        )
        
        # Should be redirected to login page
        self.assertEqual(response.status_code, 302)
        self.assertTrue('login' in response.url)
