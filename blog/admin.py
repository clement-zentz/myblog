from django.contrib import admin

from .models import Category, CategoryTranslation,\
    Author, Post, PostTranslation, Comment

# Définir une classe inline pour les traductions
class PostTranslationInline(admin.TabularInline):
    # spécifie le modèle a utiliser pour les traductions
    model = PostTranslation
    # Nombres de formulaires vides à afficher par défaut
    extra = 1

# Définir une class d'administration pour le modèle Post
# pour personnaliser l'interface admin du modèle Post
class PostAdmin(admin.ModelAdmin):
    inlines = [PostTranslationInline]
    list_display = ('id', 'get_title', 'created_date', 'updated_date', 'approved')
    list_filter = ('approved', 'created_date', 'updated_date')
    search_fields = ('translations__title', 'translations__content')
    actions = ['approve_posts', 'unapprove_posts']

    def get_title(self, obj):
        return obj.translations.first().title\
            if obj.translations.exists()\
            else 'No translation'
    get_title.short_description = 'Title'

    def approve_posts(self, request, queryset):
        queryset.update(approved=True)
    approve_posts.short_description = 'Approve selected posts'

    def unapprove_posts(self, request, queryset):
        queryset.update(approved=False)
    unapprove_posts.short_description = 'Unapprove selected posts'

class CategoryTranslationInline(admin.TabularInline):
    model = CategoryTranslation 
    extra = 1

class CategoryAdmin(admin.ModelAdmin):
    inlines = [CategoryTranslationInline]
    list_display = ('id', 'get_name')
    search_fields = ('translations__name',)

    def get_name(self, obj):
        return obj.translations.first().name\
            if obj.translations.exists()\
            else 'No translation'
    get_name.short_description = 'Name'

# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Author)
# Enregistre le modele Post 
# avec la classe d'administration PostAdmin
admin.site.register(Post, PostAdmin)
# Enregistre le modele PostTranslation
# pour qu'il soit disponible dans l'interface d'admin
admin.site.register(PostTranslation)
admin.site.register(Comment)

# TODO afficher le titre des posts dans 
# l'interface admin en fonction de la langue.