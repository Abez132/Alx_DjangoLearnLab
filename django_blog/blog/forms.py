from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post


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


class PostForm(forms.ModelForm):
    """
    Form for creating and editing blog posts.
    """
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title...'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'Write your blog post content here...'
            })
        }