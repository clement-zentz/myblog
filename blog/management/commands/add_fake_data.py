from django.core.management.base import BaseCommand
from blog.models import Post, PostTranslation,\
    Author, Category, CategoryTranslation, Comment
from django.contrib.auth.models import User
from django.db import transaction
from django.utils import timezone

from faker import Faker
import random
from decouple import config

class Command(BaseCommand):
    help = 'Ajouter des données dans la base'
    # use transaction to rollback errors
    @transaction.atomic
    def handle(self, *args, **kwargs):
        try:
            fake_en = Faker("en_EN")
            fake_fr = Faker("fr_FR")

            #---------- User ----------
            for _ in range(12):
                username_n = fake_en.name()
                password_n = fake_en.password()
                
                user_n = User.objects.create_user(
                    username=username_n, 
                    password=password_n
                )

                self.stdout.write(
                    self.style.SUCCESS(
                        f'User "{user_n.username}" created'
                    )
                )
            #---------------------------

            #---------- Author ----------
            users_5 = User.objects.filter(
                is_staff=False,
                is_superuser=False
            )[:5]
            for item in users_5:
                bio_n = fake_en.sentences()
                ppn = fake_en.image_url()
                author_n = Author.objects.create(
                    user=item,
                    bio=bio_n,
                    profile_picture=ppn
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Author "{author_n.user.username}" created'
                    )
                )
            #-----------------------------

            #---------- Category ----------
            for _ in range(8):
                # Base category model
                category_n = Category.objects.create()

                # English category
                name_en = fake_en.word()
                description_en = fake_en.sentences()
                category_en = CategoryTranslation.objects.create(
                    category = category_n,
                    language_code = 'en',
                    name = name_en,
                    description = description_en)
                
                # French category
                name_fr = fake_fr.word()
                description_fr = fake_fr.sentences()
                category_fr = CategoryTranslation.objects.create(
                    category = category_n,
                    language_code = 'fr',
                    name = name_fr,
                    description = description_fr)

                # display insertion
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Category "{category_en.name}" created'
                        f'Category "{category_fr.name}" created'
                    )
                )
            #-----------------------------

            #---------- Post ----------
            authors = Author.objects.all()
            categories = Category.objects.exclude(name='News')
            for _ in range(50):
                published_date_n = timezone.now()
                approved_n = fake_en.boolean()
                author_n = random.choice(authors)
                category_n = random.choice(categories)
                #----------------
                post_n = Post.objects.create(
                    published_date=published_date_n,
                    approved=approved_n,
                    author=author_n,
                )
                post_n.category.add(category_n)

                # English post translation
                title_en = fake_en.sentence()
                content_en = fake_en.paragraph(nb_sentences=10)
                post_en = PostTranslation.objects.create(
                    post=post_n, 
                    language_code='en', 
                    title=title_en, 
                    content=content_en)
                # French post translation
                title_fr = fake_fr.sentence()
                content_fr = fake_fr.paragraph(nb_sentences=10)
                post_fr = PostTranslation.objects.create(
                    post=post_n, 
                    language_code='fr', 
                    title=title_fr, 
                    content=content_fr)

                self.stdout.write(
                    self.style.SUCCESS(
                        f'Post "{post_en.title}" created'
                        f'Post "{post_fr.title}" created'
                    )
                )
            #----------------------------
            
            #---------- Comment ----------
            users = User.objects.all()
            posts = Post.objects.all()
            for _ in range(10):
                content_n = fake_en.paragraph(nb_sentences=5)
                post_n = random.choice(posts)
                author_n = random.choice(users)
                approved_n = fake_en.boolean()
                Comment.objects.create(
                    content=content_n,
                    approved=approved_n,
                    post=post_n,
                    author=author_n
                )
            #-----------------------------

        except Exception as e:
            transaction.set_rollback(True)
            self.stdout.write(
                self.style.ERROR(
                    f'Error adding fake_en data: {e}'
                )
            )
        