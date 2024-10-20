from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# models free of foreign key first.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name
    
class Author(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics/', blank=True)
    
    def clean(self):
        if self.bio and len(self.bio) > 500:
            raise ValidationError(
                _('Bio size = %(val)s > %(max)s characters.'),
                code="bio_too_long",
                params={"val": len(self.bio), "max": 500})

    def __str__(self):
        return self.user.username
    
# TODO ajouter un mécanisme de notifications :
# - pour les utilisateurs lambda
# - pour l'administrateur
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    approved = models.BooleanField(default=False)
    thumbnail=models.ImageField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True) 
    published_date = models.DateTimeField(
        default=timezone.now, blank=True)
    updated_date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(
        Category, related_name='posts')
    
    def __str__(self):
        return self.title

# TODO revoir les commentaires :
# ajouter, modifier, supprimer, répondre(<==>tchat)
class Comment(models.Model):
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)
    post = models.ForeignKey(
        Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE)
    
    def clean(self):
        if len(self.content) > 255: 
            raise ValidationError(
                _('Comment size = %(val)s > %(max)s characters.'),
                code="comment_too_long",
                params={"val": len(self.content), "max": 255})
        
    def __str__(self):
        return f'Comment by {self.author.username}\
            on {self.post.title}'
