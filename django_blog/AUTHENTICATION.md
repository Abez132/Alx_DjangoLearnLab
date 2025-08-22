# Django Blog Authentication System

This document provides detailed information about the authentication system implemented for the Django blog project.

## Overview

The authentication system includes the following features:
- User registration with email
- User login and logout
- User profile management
- Secure password handling
- CSRF protection
- Dedicated static files for authentication pages

## Components

### Forms

#### CustomUserCreationForm
Extends Django's built-in `UserCreationForm` to include an email field during registration.

Fields:
- Username
- Email
- Password
- Password confirmation

#### UserProfileForm
Allows authenticated users to update their profile information.

Fields:
- Username (read-only)
- Email
- First name
- Last name

### Views

#### register
Handles user registration using the `CustomUserCreationForm`.

Process:
1. Display registration form
2. Validate form data
3. Create new user account
4. Log in the new user
5. Redirect to the home page

#### user_login
Handles user login using Django's built-in `AuthenticationForm`.

Process:
1. Display login form
2. Validate credentials
3. Log in the user
4. Redirect to the home page

#### user_logout
Handles user logout.

Process:
1. Log out the user
2. Display logout message
3. Redirect to the home page

#### profile
Allows authenticated users to view and edit their profile.

Process:
1. Display profile form with current user data
2. Handle form submission for updates
3. Save updated profile information
4. Display success message

### Templates

#### base.html
Includes navigation links for authentication:
- Login/Register links for anonymous users
- Profile/Logout links for authenticated users

#### register.html
Registration form template with:
- Username field
- Email field
- Password fields
- Form validation errors
- Link to login page

#### login.html
Login form template with:
- Username field
- Password field
- Form validation errors
- Link to registration page

#### profile.html
Profile management template with:
- Username field (read-only)
- Email field
- First name field
- Last name field
- Form validation errors

### Static Files

#### auth.css
Dedicated CSS file for authentication pages with:
- Form styling
- Button styling
- Error message styling
- Alert message styling
- Responsive design

The auth.css file is included in each authentication template to provide consistent styling across all authentication pages.

### URL Configuration

The authentication URLs are defined in `blog/urls.py`:

- `/register/` - User registration
- `/login/` - User login
- `/logout/` - User logout
- `/profile/` - User profile management

## Security Features

### Password Security
- Passwords are hashed using Django's built-in password hashing
- Password strength requirements enforced by Django's validators

### CSRF Protection
- All forms include CSRF tokens
- Django's built-in CSRF middleware protects against attacks

### Authentication Decorators
- `@login_required` decorator protects the profile view
- Anonymous users are redirected to the login page

## Testing

To test the authentication system:

1. Navigate to `/register/` to create a new account
2. Navigate to `/login/` to log in with existing credentials
3. Navigate to `/profile/` to view and edit profile information
4. Navigate to `/logout/` to log out

## Customization

To extend the user model with additional fields like a profile picture or bio:

1. Create a `UserProfile` model in `models.py`
2. Add a `OneToOneField` relationship to the User model
3. Update the `UserProfileForm` to include the new fields
4. Modify the profile template to display the new fields

Example:
```python
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
```

## Troubleshooting

Common issues and solutions:

1. **CSRF verification failed**: Ensure `{% csrf_token %}` is included in all forms
2. **Invalid form data**: Check that all required fields are filled correctly
3. **Permission denied**: Verify that the `@login_required` decorator is used appropriately
4. **Database errors**: Run migrations after making model changes