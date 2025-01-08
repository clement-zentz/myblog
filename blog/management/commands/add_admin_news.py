from django.core.management.base import BaseCommand
from blog.models import Post, PostTranslation,\
    Author, Category, CategoryTranslation, Comment
from django.contrib.auth.models import User
from django.db import transaction
from django.utils import timezone

from decouple import config

class Command(BaseCommand):
    help = 'Ajouter des données dans la base'
    # use transaction to rollback errors
    @transaction.atomic
    def handle(self, *args, **kwargs):
        try:
            # ---------- superuser ----------
            superuser_username=config("SUPERUSER_USERNAME")
            superuser_password=config("SUPERUSER_PASSWORD")
            super_user = User.objects.create_superuser(
                username=superuser_username, 
                password=superuser_password
            )

            #---------- News Post-Author ----------
            # add news Author
            super_author = Author.objects.create(
                user=super_user,
                bio="Ceci est une bio.",
                profile_picture=""
            )

            category_x = Category(id = 1000)

            category_x.save()

            CategoryTranslation.objects.create(
                category = category_x,
                language_code = 'en',
                name = "News",
                description = "Some news about the project."
            )
            CategoryTranslation.objects.create(
                category = category_x,
                language_code = 'fr',
                name = "Nouvelles",
                description = "Des nouvelles du projet."
            )

            # add news post
            current_time = timezone.now()
            news_post = Post(
                id=10000,
                published_date=current_time,
                approved=True,
                author=super_author,
            )
            news_post.save()

            news_post.category.add(category_x)

            # English translation
            PostTranslation.objects.create(
                post=news_post,
                language_code='en',
                title='Latest News',
                content='The news content.'
            )
            # French translation
            PostTranslation.objects.create(
                post=news_post,
                language_code='fr',
                title='Dernières nouvelles',
                content='Le contenu des nouvelles.'
            )

            self.stdout.write(
                self.style.SUCCESS(
                    'Toutes les données ont été ajoutées avec succès'
                )
            )

        except Exception as e:
            transaction.set_rollback(True)
            self.stdout.write(
                self.style.ERROR(
                    f'Error adding fake_en data: {e}'
                )
            )