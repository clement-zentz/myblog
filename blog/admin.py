from django.contrib import admin

from .models import Category, Author, Post,\
    PostTranslation, Comment

# Définir une classe inline pour les traductions
class PostTranslationInline(admin.TabularInline):
    # spécifie le modèle a utiliser pour les traductions
    model = PostTranslation
    # Nombres de formulaires vides à afficher par défaut
    extra = 1 

# Définir une class d'administration pour le modèle Post
# pour personnaliser l'interface admin du modèle Post
class PostAdmin(admin.ModelAdmin):
    # Ajouter les traductions en ligne
    inlines = [PostTranslationInline]

# Register your models here.
admin.site.register(Category)
admin.site.register(Author)
# Enregistre le modele Post 
# avec la classe d'administration PostAdmin
admin.site.register(Post, PostAdmin)
# Enregistre le modele PostTranslation
# pour qu'il soit disponible dans l'interface d'admin
admin.site.register(PostTranslation)
admin.site.register(Comment)