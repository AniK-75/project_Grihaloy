from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, VerificationDocument, Rating

# This is the widget needed to fix the ugly file input
from django.forms.widgets import ClearableFileInput


class CustomUserCreationForm(UserCreationForm):
    # NEW: Add a field for the secret code. It's not part of the model.
    admin_secret_code = forms.CharField(
        label="Admin Secret Code",
        required=False,  # It's only required if the role is Admin
        widget=forms.PasswordInput,  # This hides the text as it's typed
        help_text="This code is required only if registering as an ADMIN."
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'profile_picture', 'role', 'phone')

    # NEW: Add custom validation logic for the form
    def clean(self):
        # First, run the parent class's clean method
        cleaned_data = super().clean()
        role = cleaned_data.get("role")
        admin_secret_code = cleaned_data.get("admin_secret_code")

        # The secret code you provided
        SECRET_CODE = "ALAS-GRIHALOY-BANGER-DOMINATIVE-AURA-SHIELD"

        # Check the logic only if the user is trying to register as an Admin
        if role == 'ADMIN':
            if admin_secret_code != SECRET_CODE:
                # If the code is wrong, raise a validation error on that specific field
                self.add_error('admin_secret_code', "Invalid secret code for Admin registration.")

        # Always return the full collection of cleaned data.
        return cleaned_data


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