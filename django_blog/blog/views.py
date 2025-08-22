from django.shortcuts import render
from .models import Post


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
