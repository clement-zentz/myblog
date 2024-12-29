from django.core.management.base import BaseCommand
from blog.models import Post, Author, Category, Comment
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
            fake = Faker()

            #---------- User ----------
            for _ in range(12):
                username_n = fake.name()
                password_n = fake.password()
                user_n = User.objects.create_user(
                    username=username_n, password=password_n
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f'User "{user_n.username}" created'
                    )
                )
            #---------------------------

            #---------- Author ----------
            users_5 = User.objects.all()[:5]
            for item in users_5:
                bio_n = fake.sentences()
                ppn = fake.image_url()
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
            for _ in range(6):
                name_n = fake.word()
                description_n = fake.sentences()
                category_n = Category.objects.create(
                    name=name_n,
                    description=description_n
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Category "{category_n.name}" created'
                    )
                )
            #-----------------------------

            #---------- Post ----------
            authors = Author.objects.all()
            categories = Category.objects.all()
            for _ in range(50):
                title_n = fake.sentence()
                content_n = fake.paragraph(nb_sentences=5)
                published_date_n = timezone.now()
                approved_n = fake.boolean()
                author_n = random.choice(authors)
                category_n = random.choice(categories)
                #----------------
                post_n = Post.objects.create(
                    title=title_n, 
                    content=content_n,
                    published_date=published_date_n,
                    approved=approved_n,
                    author=author_n,
                )
                post_n.category.add(category_n)

                self.stdout.write(
                    self.style.SUCCESS(
                        f'Post "{post_n.title}" created'
                    )
                )
            #----------------------------
            
            #---------- Comment ----------
            users = User.objects.all()
            posts = Post.objects.all()
            for _ in range(10):
                content_n = fake.paragraph(nb_sentences=5)
                post_n = random.choice(posts)
                author_n = random.choice(users)
                approved_n = fake.boolean()
                Comment.objects.create(
                    content=content_n,
                    approved=approved_n,
                    post=post_n,
                    author=author_n
                )
            #-----------------------------

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
            news_categ = Category.objects.create(
                name="News",
                description="News Category"
            )
            # add news post
            current_time = timezone.now()
            news_post = Post(
                id=10000,
                title="Latest News:", 
                content="Replace it with real content.",
                published_date=current_time,
                approved=True,
                author=super_author,
            )
            news_post.save()
            news_post.category.add(news_categ)

        except Exception as e:
            transaction.set_rollback(True)
            self.stdout.write(self.style.ERROR(f'Error adding fake data: {e}'))
        