from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Post
from .forms import CustomUserCreationForm, UserProfileForm


def post_list(request):
    """
    View to display a list of blog posts.
    
    Args:
        request: The HTTP request object.
        
    Returns:
        HttpResponse: Rendered HTML template with blog posts.
    """
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})


def register(request):
    """
    View to handle user registration.
    
    Args:
        request: The HTTP request object.
        
    Returns:
        HttpResponse: Rendered HTML template for registration.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            login(request, user)
            return redirect('post_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})


def user_login(request):
    """
    View to handle user login.
    
    Args:
        request: The HTTP request object.
        
    Returns:
        HttpResponse: Rendered HTML template for login.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('post_list')
    else:
        form = AuthenticationForm()
    return render(request, 'blog/login.html', {'form': form})


def user_logout(request):
    """
    View to handle user logout.
    
    Args:
        request: The HTTP request object.
        
    Returns:
        HttpResponse: Redirect to post list after logout.
    """
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('post_list')


@login_required
def profile(request):
    """
    View to display and edit user profile.
    
    Args:
        request: The HTTP request object.
        
    Returns:
        HttpResponse: Rendered HTML template for profile.
    """
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'blog/profile.html', {'form': form})
