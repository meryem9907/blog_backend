from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from .models import Post
from users.models import Author

class CommentTest(APITestCase):
    def setUp(self):
        self.reader_client = APIClient()

    def authenticate(self):
        self.client = APIClient()
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
        
    def create_comments(self):
        self.create_posts()
        data = {"body": "Nice post!",  "guestname": "bob",  "created_at": "2025-10-28T09:30:00Z" }
        response = self.reader_client.post(path='/comment/create/1/', data=data, 
                         content_type="application/json")
        self.assertEqual(response.status_code, 201)

        data2 = {"body": "Author here thanks for reading!", "guestname": "bob",  "created_at": "2025-10-28T09:35:00Z" }
        response = self.reader_client.post(path='/comment/create/1/', data=data2, 
                         content_type="application/json")
        self.assertEqual(response.status_code, 201)

        
    def test_create_without_auth(self):
        self.create_posts()
        data = {"body": "Nice post!",  "guestname": "bob",  "created_at": "2025-10-28T09:30:00Z" }
        response = self.reader_client.post(path='/comment/create/1/', data=data, 
                         content_type="application/json")
        self.assertEqual(response.status_code, 201)


    def test_delete(self):
        self.create_posts()
        response = self.client.delete(path='/post/delete/1/', 
                         content_type="application/json")
        self.assertEqual(response.status_code, 204)
        response = self.client.get(path='/post/read/1/', 
                         content_type="application/json")
        self.assertEqual(response.status_code, 404)
        
    def test_list_comments(self):
        self.create_comments()
        response = self.reader_client.get(path='/comment/list/1/', 
                         content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_comment(self):
        self.create_comments()
        response = self.reader_client.get(path='/comment/read/1/', 
                         content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["guestname"], "bob")






