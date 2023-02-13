from django.test import TestCase
from .models import Posts
from django.contrib.auth.models import User
# Create your tests here.

class BlogTest(TestCase):
    @classmethod
    def setUpTestData(cls):

        test_post = Posts.objects.create(title = 'Hello',content = 'Hello123')
        test_post.save()
    
    def test_blog_content(self):
        post = Posts.objects.get(id = 1)
        title = f'{post.title}'
        content = f'{post.content}'
        self.assertEqual(title,'Hello')
        self.assertEqual(content,'Hello123')
