from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    """
    Custom user creation form that extends Django's built-in UserCreationForm.
    Adds an email field to the registration form.
    """
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        """
        Save the user with the email field.
        
        Args:
            commit (bool): Whether to save the user to the database.
            
        Returns:
            User: The saved user instance.
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    """
    Form for editing user profile information.
    """
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")
        
    def __init__(self, *args, **kwargs):
        """
        Initialize the form and make the username field read-only.
        """
        super().__init__(*args, **kwargs)
        # Make username read-only
        self.fields['username'].widget.attrs['readonly'] = True