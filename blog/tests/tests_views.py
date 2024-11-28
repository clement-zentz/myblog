from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from blog.models import Post, Comment, Author, Category

class BlogViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.author = Author.objects.create(user=self.user, bio='This is a test bio.', profile_picture='')
        self.post = Post.objects.create(
            title='Test Post',
            content='This is a test post.',
            author=self.author,
            approved=True,
            published_date=timezone.now()
        )

    def test_post_list_view(self):
        # reverse(app_name:url_name)
        response = self.client.get(reverse('blog:post-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_list.html')
        self.assertContains(response, 'Test Post')

    def test_post_detail_view(self):
        response = self.client.get(reverse('blog:post-detail', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_detail.html')
        self.assertContains(response, 'Test Post')

    def test_home_view(self):
        response = self.client.get(reverse('blog:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/home.html')

    def test_about_view(self):
        response = self.client.get(reverse('blog:about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/about.html')

    def test_contact_view(self):
        response = self.client.get(reverse('blog:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/contact.html')
