from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, VerificationDocument, Rating

# This is the widget needed to fix the ugly file input
from django.forms.widgets import ClearableFileInput

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'profile_picture', 'role', 'phone')

# This is the form for editing a user's profile, now correctly named
class ProfileEditForm(UserChangeForm):
    # We remove the password fields so users can't change passwords here
    password = None

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone', 'profile_picture')

        # THIS IS THE FIX: This widget removes the "Currently:..." text
        widgets = {
            'profile_picture': ClearableFileInput(),
        }

class VerificationDocumentForm(forms.ModelForm):
    class Meta:
        model = VerificationDocument
        fields = ('doc', 'doc_type')

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ('score', 'review')