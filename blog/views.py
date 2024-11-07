from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from .models import Post, Comment
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView

# Create your views here.
# Vue pour lister tous les articles de blog
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']

    # [:5] return five blog post approved
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(approved=True)
        return queryset[:15]

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = "post"

def about(request):
    return render(request, 'blog/about.html')

def contact(request):
    return render(request, 'blog/contact.html')