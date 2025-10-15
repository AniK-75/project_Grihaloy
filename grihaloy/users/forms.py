from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, VerificationDocument, Rating

class CustomUserCreationForm(UserCreationForm):
    # --- ADDED PROFILE PICTURE FIELD ---
    profile_picture = forms.ImageField(required=False, help_text='Optional. Choose a profile picture.')

    class Meta:
        model = CustomUser
        # --- ADDED 'profile_picture' TO FIELDS ---
        fields = ('username', 'email', 'profile_picture', 'role', 'phone', 'password1', 'password2')

# --- NEW FORM FOR PROFILE EDITING ---
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone', 'profile_picture')


# --- NO CHANGES TO OTHER FORMS ---
class VerificationDocumentForm(forms.ModelForm):
    class Meta:
        model = VerificationDocument
        fields = ('doc', 'doc_type')

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ('score', 'review')
