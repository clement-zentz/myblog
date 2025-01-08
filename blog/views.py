from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from .models import Post, PostTranslation, Comment, Category, CategoryTranslation 
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.urls import reverse
# translation
from django.utils import translation

# MTV (Model-Template-View)
# MVC (Model-View-Controller)
# Model == Model,
# Template == View, 
# View == Controller.
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    # var name inside template
    context_object_name = 'posts'
    ordering = ['-published_date']

    def get_queryset(self):
        queryset = super().get_queryset()\
            .filter(approved=True)\
            .exclude(id=10000)
        language_code = translation.get_language()
        post_translations = PostTranslation.objects.filter(
            post__in=queryset, language_code=language_code
        )
        return post_translations[:14]

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    # context variable name
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language_code = translation.get_language()
        # Post list translated
        post_translation = get_object_or_404(
            PostTranslation,
            post=self.get_object(),
            language_code=language_code
        )
        # add key, value paire to context dict
        context['post_translation'] = post_translation
        # Post category list translated
        post_categories = self.get_object().category.exclude(id=1000)
        categ_tr_list = []
        for category in post_categories:
            categ_tr = get_object_or_404(
                CategoryTranslation,
                category=category,
                language_code=language_code
            )
            categ_tr_list.append(categ_tr)
        # add key, value paire to context dict
        context['p_categ_tr'] = categ_tr_list
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
    language_code = translation.get_language()
    post_translation = get_object_or_404(
        PostTranslation, 
        post=post, 
        language_code=language_code
    )
    return render(
        request, 
        'blog/news.html', 
        {
            'post' : post, 
            'post_translation': post_translation
        }
    )