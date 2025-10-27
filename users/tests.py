from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from .models import Author

class RegistrationTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
    
    def test_register_author_successfull(self):
        response = self.client.post(path='/auth/register/', data={"username":"alice","email":"alice@example.com","password":"StrongPass123!","password2":"StrongPass123!"}, 
                         content_type="application/json")
        self.assertEqual(response.status_code, 201)
    
    def test_register_author_with_invalid_data(self):
        # missing email, username, password
        response = self.client.post(path='/auth/register/', data={"username":"alice","password":"StrongPass123!","password2":"StrongPass123!"}, 
                         content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["email"][0], "This field is required.")
        # check if other keys return an error too
        with self.assertRaises(KeyError):
            self.assertEqual(response.data["username"][0], "This field is required.")

        
        response = self.client.post(path='/auth/register/', data={"email":"alice@example.com", "password":"StrongPass123!","password2":"StrongPass123!"}, 
                         content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["username"][0], "This field is required.")
        
        response = self.client.post(path='/auth/register/', data={"username":"alice","email":"alice@example.com"}, 
                         content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["password"][0], "This field is required.")
        self.assertEqual(response.data["password2"][0], "This field is required.")


class LoginTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        response = self.client.post(path='/auth/register/', data={"username":"alice","email":"alice@example.com","password":"StrongPass123!","password2":"StrongPass123!"}, 
                         content_type="application/json")
        self.assertEqual(response.status_code, 201)

    def test_login_successfull(self):
        login_response = self.client.post("/auth/login/", {"email": "alice@example.com", "password": "StrongPass123!"}, content_type="application/json")
        self.assertEqual(login_response.status_code, 200)

    def test_login_with_invalid_data(self):
        # invalid email, password 
        login_response = self.client.post("/auth/login/", {"email": "john@example.com", "password": "StrongPass123!"}, content_type="application/json")
        self.assertEqual(login_response.status_code, 401)
        login_response = self.client.post("/auth/login/", {"email": "alice@example.com", "password": "WrongPass123!"}, content_type="application/json")
        self.assertEqual(login_response.status_code, 401)


class LogoutDeleteRetrieveAndUpdateTest(APITestCase):
    def setUp(self):
        self.author = Author.objects.create_user(
            username="alice",
            email="alice@example.com",
            password="StrongPass123!"
        )
        self.client = APIClient()
        # login
        login_response = self.client.post("/auth/login/", {"email": "alice@example.com", "password": "StrongPass123!"}, content_type="application/json")
        self.assertEqual(login_response.status_code, 200)
        # set tokens
        self.access = login_response.data["access"]
        self.refresh = login_response.data["refresh"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")

    def test_logout_successfull(self):
        response = self.client.post(path="/auth/logout/", data={"refresh":self.refresh},
                                    content_type="application/json" )
        self.assertEqual(response.status_code, 205)
        login_response_with_old_refresh = self.client.post("/auth/refresh/", {"refresh":self.refresh}, content_type="application/json")
        self.assertEqual(login_response_with_old_refresh.status_code, 404)

    def test_delete_author(self):
        response = self.client.delete(path="/auth/delete/user/", 
                                    content_type="application/json" )
        self.assertEqual(response.status_code, 204)
        login_response = self.client.post("/auth/login/", {"email": "alice@example.com", "password": "StrongPass123!"}, content_type="application/json")
        self.assertEqual(login_response.status_code, 401)

    def test_update_author(self):
        response = self.client.patch("/auth/update/user/", {"email": "new_alice@example.com"}, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["email"], "new_alice@example.com")

    def test_retrieve_author(self):
        response = self.client.get("/auth/me/", content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["email"], "alice@example.com")




