from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, UserPantry, RecipeReview

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio']

class UserPantryForm(forms.ModelForm):
    class Meta:
        model = UserPantry
        fields = ['ingredient', 'expiration_date', 'image_url']

class RecipeReviewForm(forms.ModelForm):
    class Meta:
        model = RecipeReview
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class': 'border rounded p-2 mb-2 w-full'}),
            'comment': forms.Textarea(attrs={'class': 'border rounded p-2 mb-2 w-full', 'rows': 4}),
        }  

