from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from .models import Post
from users.models import Author

class PostTest(APITestCase):
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

    def create_posts(self):
        self.authenticate()
        # create 2 posts
        data = {"title": "My First Blog Post","body": "This is the content of the post.","status": "DRAFT","created_at": "2025-10-18T09:30:00Z"}
        self.client.post(path='/post/create/', data=data, 
                         content_type="application/json")
        data2 = {"title": "My Second Blog Post", "body": "This is the content of the post.", "status": "DRAFT", "created_at": "2025-10-28T09:30:00Z" }
        self.client.post(path='/post/create/', data=data2, 
                         content_type="application/json")
        
    def test_create_without_auth(self):
        data = {"title": "My First Blog Post","body": "This is the content of the post.","status": "DRAFT","created_at": "2025-10-18T09:30:00Z"}
        response = self.client.post(path='/post/create/', data=data, 
                         content_type="application/json")
        self.assertEqual(response.status_code, 401)

    def test_create_with_auth(self):
        self.authenticate()
        data = {"title": "My First Blog Post","body": "This is the content of the post.","status": "DRAFT","created_at": "2025-10-18T09:30:00Z"}
        response = self.client.post(path='/post/create/', data=data, 
                         content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["title"], "My First Blog Post")

    def test_create_with_invalid_data(self):
        self.authenticate()
        data = {"title": "My First Blog Post","body": "This is the content of the post.","status": "DRAFT","created_at": "2025-10-18T09:30:00Z", "published_at": "2025-10-18T09:30:00Z"}
        response = self.client.post(path='/post/create/', data=data, 
                         content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_delete(self):
        self.create_posts()
        response = self.client.delete(path='/post/delete/1/', 
                         content_type="application/json")
        self.assertEqual(response.status_code, 204)
        response = self.client.get(path='/post/read/1/', 
                         content_type="application/json")
        self.assertEqual(response.status_code, 404)

    def test_update(self):
        self.create_posts()
        data = {"status": "PUBLIC","created_at": "2025-10-18T09:30:00Z", "published_at": "2025-10-18T09:30:00Z"}
        response = self.client.patch(path='/post/update/1/', data=data, 
                         content_type="application/json")
        self.assertEqual(response.status_code, 200)
        
    def test_list_posts(self):
        self.create_posts()
        reader_client = APIClient() # not authenticated client
        response = reader_client.get(path='/post/list/', 
                         content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_posts(self):
        self.create_posts()
        reader_client = APIClient() # not authenticated client
        response = reader_client.get(path='/post/read/1/', 
                         content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "My First Blog Post")





