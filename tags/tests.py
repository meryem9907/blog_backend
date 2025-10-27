from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from .models import Post
from users.models import Author

class TagTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def authenticate(self):
        self.author = Author.objects.create_user(
            username="alice",
            email="alice@example.com",
            password="StrongPass123!"
        )
        # login
        login_response = self.client.post("/auth/login/", {"email": "alice@example.com", "password": "StrongPass123!"}, content_type="application/json")
        self.assertEqual(login_response.status_code, 200)
        # set tokens
        self.access = login_response.data["access"]
        self.refresh = login_response.data["refresh"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")

    def create_tags(self):
        self.authenticate()
        # create 2 tags
        data = { "name": "Ruby",  "slug": "ruby"}
        self.client.post(path='/tags/create/', data=data, 
                         content_type="application/json")
        data2 = { "name": "Python",  "slug": "python"}
        self.client.post(path='/tags/create/', data=data2, 
                         content_type="application/json")
    def create_posts(self):
        # create 2 posts
        data = {"title": "My First Blog Post","body": "This is the content of the post.","status": "DRAFT","created_at": "2025-10-18T09:30:00Z"}
        self.client.post(path='/post/create/', data=data, 
                         content_type="application/json")
        data2 = {"title": "My Second Blog Post", "body": "This is the content of the post.", "status": "DRAFT", "created_at": "2025-10-28T09:30:00Z" }
        self.client.post(path='/post/create/', data=data2, 
                         content_type="application/json")
    
    def create_post_tags(self):
        self.create_tags()
        self.create_posts()
        response = self.client.post(path='/tags/create/tag/1/post/1/',
                         content_type="application/json")
        self.assertEqual(response.status_code, 201)
        response = self.client.post(path='/tags/create/tag/2/post/2/',
                         content_type="application/json")
        self.assertEqual(response.status_code, 201)

        
    def test_create_without_auth(self):
        data = { "name": "Ruby",  "slug": "ruby"}
        response = self.client.post(path='/tags/create/', data=data, 
                         content_type="application/json")
        self.assertEqual(response.status_code, 401)

    def test_create_with_auth(self):
        self.authenticate()
        data = { "name": "Ruby",  "slug": "ruby"}
        response = self.client.post(path='/tags/create/', data=data, 
                         content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name"], "Ruby")

     
    def test_create_post_tags(self):
        self.create_tags()
        self.create_posts()
        response = self.client.post(path='/tags/create/tag/1/post/1/',
                         content_type="application/json")
        self.assertEqual(response.status_code, 201)

    
    def test_delete(self):
        self.create_post_tags()
        # deleting tags should delete post_tag
        response = self.client.delete(path='/tags/delete/1/', 
                         content_type="application/json")
        self.assertEqual(response.status_code, 204)
        response = self.client.get(path='/tags/list/post-tags/1/', 
                         content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)
   
        
    def test_list_post_tags(self):
        self.create_post_tags()
        reader_client = APIClient() # not authenticated client
        response = reader_client.get(path='/tags/list/post-tags/1/', 
                         content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    
    def test_list_tags(self):
        self.create_tags()
        reader_client = APIClient() # not authenticated client
        response = reader_client.get(path='/tags/list/', 
                         content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2) 


