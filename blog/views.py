from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from .models import Post, Comment
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.urls import reverse

# Create your views here.
# Vue pour lister tous les articles de blog
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']

    # [:5] return five blog post approved
    def get_queryset(self):
        queryset = super().get_queryset()\
        .filter(approved=True)\
        .exclude(id=10000)
        return queryset[:14]

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = "post"

def home(request):
    context = { 
        # variable de context (home_url)
        'home_url': reverse('blog:home') 
    }
    return render(request, 'blog/home.html', context)

def about(request):
    return render(request, 'blog/about.html')

def contact(request):
    return render(request, 'blog/contact.html')

def news(request):
    post = get_object_or_404(Post, id=10000)
    return render(request, 'blog/news.html', {'post' : post})