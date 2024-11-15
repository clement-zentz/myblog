from django.urls import path

from . import views

app_name = "blog"
urlpatterns = [
    path('', views.home, name='home'),
    path('post-list/', views.PostListView.as_view(), name="post-list"),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('<int:pk>/', views.PostDetailView.as_view(), name="post-detail"),
]