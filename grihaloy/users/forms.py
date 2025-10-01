from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, VerificationDocument, Rating

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role', 'phone', 'password1', 'password2')

class VerificationDocumentForm(forms.ModelForm):
    class Meta:
        model = VerificationDocument
        fields = ('doc', 'doc_type')

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        # we'll set rater and rated in the view, so exclude them
        fields = ('score', 'review')
