from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils import timezone
# from ...models import Category, Post, Author, Comment
from blog.models import Category, Post, Author, Comment

class CategoryModelTest(TestCase):

    def test_category_name_unique(self):
        Category.objects.create(
            name="Category1",
            description="This is a description.")
        with self.assertRaises(Exception):
            Category.objects.create(
                name="Category1",
                description="Another description.")
    
    def test_category_description_blank(self):
        category = Category.objects.create(
            name="Category1", description="")
        self.assertEqual(category.description, "")

class AuthorModelTest(TestCase):
    # an Author need one User instance
    def setUp(self):
        self.user1 = User.objects.create(
            username="user1",
            password="user1_password")
    
    def test_author_bio_blank(self):
        author1 = Author.objects.create(
            user=self.user1,
            bio="",
            profile_picture="")
        self.assertEqual(author1.bio, "")

    def test_author_bio_too_long(self):
        author1 = Author.objects.create(
            user=self.user1,
            bio="a"*501,
            profile_picture="")
        with self.assertRaises(ValidationError):
            author1.clean()
    
    def test_author_bio_correct(self):
        author1 = Author.objects.create(
            user=self.user1,
            bio="b"*500)
        try:
            author1.clean()
        except ValidationError:
            self.fail("ValidationError raised unexpectedly!")

class PostModelTest(TestCase):
    # a post need one author instance
    def setUp(self):
        # User model has 2 required fields: 
        # username(==login) and password
        user1 = User.objects.create(
            username="user1", password="mypassword")
        
        self.author1 = Author.objects.create(
            user=user1, 
            bio="this is author1 bio.",
            profile_picture="")
        
    def test_post_future_published_date(self):
        future_date = timezone.now() + timezone.timedelta(days=1)
        post1 = Post.objects.create(
            title="Future post",
            content="this is a future post.",
            published_date=future_date,
            author=self.author1)
        self.assertEqual(post1.published_date, future_date)

    def test_post_multiple_categories(self):
        category1 = Category.objects.create(
            name="Category 1 name", 
            description="Category 1 description.")
        category2 = Category.objects.create(
            name="Category 2 name", 
            description="Category 2 description.")
        post1 = Post.objects.create(
            title="Multi-category post",
            content="this post has multiple categories.",
            published_date=timezone.now(),
            author=self.author1)
        post1.category.add(category1, category2)
        self.assertEqual(post1.category.count(), 2)
        self.assertEqual(post1.category.all()[0].name, category1.name)
        self.assertEqual(post1.category.all()[1].name, category2.name)

    def test_post_cascade_delete(self):
        post1 = Post.objects.create(
            title="Test post",
            content="This is a test post.",
            author=self.author1,
            published_date=timezone.now())
        self.author1.delete()
        self.assertFalse(Post.objects.contains(post1))
        self.assertFalse(
            Post.objects.filter(id=post1.id).exists())

class CommentModelTest(TestCase):
    # a comment need one author, 
    # one user and one post instance
    def setUp(self):
        user1 = User.objects.create(
            username="user1", password="user1_password")
        self.user2 = User.objects.create(
            username="user2", password="user2_password")
        
        post_author = Author.objects.create(
            user=user1, 
            bio="this is author1 bio.",
            profile_picture="")
        
        self.post1 = Post.objects.create(
            title="Multi-category post",
            content="this post has multiple categories.",
            published_date=timezone.now(),
            author=post_author)

    def test_comment_too_long(self):
        comment1 = Comment.objects.create(
            content='c'*256,
            post=self.post1,
            author=self.user2)
        with self.assertRaises(ValidationError):
            comment1.clean()
    
    def test_comment_correct(self):
        comment1 = Comment.objects.create(
            content='c'*255,
            post=self.post1,
            author=self.user2)
        try:
            comment1.clean()
        except ValidationError:
            self.fail("ValidationError raised unexpectedly!")
    
    def test_comment_approval(self):
        comment1 = Comment.objects.create(
            content="this is a test comment.",
            post=self.post1,
            author=self.user2)
        comment1.approved = True
        comment1.save()
        self.assertTrue(comment1.approved)

    def test_comment_cascade_delete(self):
        comment1 = Comment.objects.create(
            content="This is a test comment.",
            post=self.post1,
            author=self.user2)
        self.post1.delete()
        self.assertFalse(
            Comment.objects.filter(id=comment1.id).exists())