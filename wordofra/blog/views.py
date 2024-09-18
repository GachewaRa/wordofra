# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.is_restricted and not request.user.is_authenticated:
        return render(request, 'blog/restricted_post.html')
    return render(request, 'blog/post_detail.html', {'post': post})



def home(request):
    return render(request, 'blog/home.html')
