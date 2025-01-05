from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from .models import Post, Comment
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.urls import reverse
# translation
from django.utils import translation
from .models import Post, PostTranslation

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
        language_code = translation.get_language()
        post_translation = PostTranslation.objects.filter(
            post__in=queryset, language_code=language_code
        )
        return post_translation[:14]

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language_code = translation.get_language()
        post_translation = get_object_or_404(
            PostTranslation, 
            post=self.get_object,
            language_code=language_code
        )
        context['post_translation'] = post_translation
        return context

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