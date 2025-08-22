from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from .models import Post, Comment
from .forms import CustomUserCreationForm, UserProfileForm, PostForm, CommentForm


class PostListView(ListView):
    """
    View to display a list of all blog posts.
    Accessible to all users (no authentication required).
    """
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 10


class PostDetailView(DetailView):
    """
    View to display a single blog post in detail with comments.
    Accessible to all users (no authentication required).
    """
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        """Add comments and comment form to the context."""
        context = super().get_context_data(**kwargs)
        # Get all comments for this post
        context['comments'] = self.object.comments.all().order_by('created_at')
        # Add comment form for authenticated users
        if self.request.user.is_authenticated:
            context['comment_form'] = CommentForm()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """
    View to create a new blog post.
    Only authenticated users can access this view.
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post_list')
    
    def form_valid(self, form):
        """Set the author to the current user before saving."""
        form.instance.author = self.request.user
        messages.success(self.request, 'Blog post created successfully!')
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View to edit an existing blog post.
    Only the author of the post can edit it.
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post_list')
    
    def test_func(self):
        """Check if the current user is the author of the post."""
        post = self.get_object()
        return self.request.user == post.author
    
    def form_valid(self, form):
        """Display success message after updating."""
        messages.success(self.request, 'Blog post updated successfully!')
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    View to delete a blog post.
    Only the author of the post can delete it.
    """
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')
    
    def test_func(self):
        """Check if the current user is the author of the post."""
        post = self.get_object()
        return self.request.user == post.author
    
    def delete(self, request, *args, **kwargs):
        """Display success message after deletion."""
        messages.success(request, 'Blog post deleted successfully!')
        return super().delete(request, *args, **kwargs)


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


# Comment Views

class CommentCreateView(LoginRequiredMixin, CreateView):
    """
    View to create a new comment on a blog post.
    Only authenticated users can access this view.
    """
    model = Comment
    form_class = CommentForm
    template_name = 'blog/add_comment.html'
    
    def form_valid(self, form):
        """Set the author and post before saving."""
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.author = self.request.user
        form.instance.post = post
        messages.success(self.request, 'Comment added successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        """Redirect to the post detail page after creating comment."""
        return reverse('post_detail', kwargs={'pk': self.kwargs['pk']})
    
    def get_context_data(self, **kwargs):
        """Add post to the context."""
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, pk=self.kwargs['pk'])
        return context


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View to edit an existing comment.
    Only the comment author can edit it.
    """
    model = Comment
    form_class = CommentForm
    template_name = 'blog/edit_comment.html'
    
    def test_func(self):
        """Check if the current user is the author of the comment."""
        comment = self.get_object()
        return self.request.user == comment.author
    
    def form_valid(self, form):
        """Display success message after updating."""
        messages.success(self.request, 'Comment updated successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        """Redirect to the post detail page after updating comment."""
        return reverse('post_detail', kwargs={'pk': self.object.post.pk})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    View to delete a comment.
    Only the comment author can delete it.
    """
    model = Comment
    template_name = 'blog/delete_comment.html'
    
    def test_func(self):
        """Check if the current user is the author of the comment."""
        comment = self.get_object()
        return self.request.user == comment.author
    
    def delete(self, request, *args, **kwargs):
        """Display success message after deletion."""
        messages.success(request, 'Comment deleted successfully!')
        return super().delete(request, *args, **kwargs)
    
    def get_success_url(self):
        """Redirect to the post detail page after deleting comment."""
        return reverse('post_detail', kwargs={'pk': self.object.post.pk})


@login_required
def add_comment(request, post_id):
    """
    Function-based view to add a comment to a post via AJAX or form submission.
    """
    post = get_object_or_404(Post, pk=post_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return HttpResponseRedirect(reverse('post_detail', kwargs={'pk': post_id}))
    else:
        form = CommentForm()
    
    return render(request, 'blog/add_comment.html', {
        'form': form,
        'post': post
    })
