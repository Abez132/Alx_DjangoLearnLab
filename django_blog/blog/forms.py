from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment, Tag


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
    tags_input = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter tags separated by commas (e.g., django, python, web-development)'
        }),
        help_text='Separate multiple tags with commas'
    )
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title...'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'Write your blog post content here...'
            }),
            'tags': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'style': 'display: none;'  # Hide the default widget
            })
        }
    
    def __init__(self, *args, **kwargs):
        """Initialize the form with existing tags."""
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            # For editing, populate tags_input with existing tags
            self.fields['tags_input'].initial = ', '.join([tag.name for tag in self.instance.tags.all()])
    
    def clean_tags_input(self):
        """Clean and process the tags input field."""
        tags_input = self.cleaned_data.get('tags_input', '').strip()
        if not tags_input:
            return []
        
        # Split by comma and clean each tag
        tag_names = [name.strip() for name in tags_input.split(',') if name.strip()]
        
        # Validate tag length
        for tag_name in tag_names:
            if len(tag_name) > 50:
                raise forms.ValidationError(f'Tag "{tag_name}" is too long. Maximum length is 50 characters.')
            if len(tag_name) < 2:
                raise forms.ValidationError(f'Tag "{tag_name}" is too short. Minimum length is 2 characters.')
        
        return tag_names
    
    def save(self, commit=True):
        """Save the post and create/update tags."""
        post = super().save(commit=False)
        
        if commit:
            post.save()
            
            # Clear existing tags
            post.tags.clear()
            
            # Get cleaned tag names
            tag_names = self.cleaned_data.get('tags_input', '').strip()
            if tag_names:
                # Split and process tags
                tag_names = [name.strip() for name in tag_names.split(',') if name.strip()]
                
                # Create or get existing tags
                for tag_name in tag_names:
                    tag, created = Tag.objects.get_or_create(name=tag_name.lower())
                    post.tags.add(tag)
            
            # Save many-to-many relationships
            self.save_m2m()
        
        return post


class CommentForm(forms.ModelForm):
    """
    Form for creating and editing comments on blog posts.
    """
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your comment here...',
                'maxlength': 1000
            })
        }
        labels = {
            'content': 'Comment'
        }
    
    def __init__(self, *args, **kwargs):
        """
        Initialize the form with custom styling and validation.
        """
        super().__init__(*args, **kwargs)
        self.fields['content'].help_text = 'Maximum 1000 characters'
    
    def clean_content(self):
        """
        Validate comment content.
        """
        content = self.cleaned_data.get('content')
        if not content or len(content.strip()) < 5:
            raise forms.ValidationError('Comment must be at least 5 characters long.')
        return content.strip()