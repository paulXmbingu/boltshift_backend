from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()

class CustomerRegistrationTest(TestCase):
    def test_customer_registration(self):
        client = APIClient()
        data = {
            "email": "testuser@example.com",
            "first_name":"test",
            "last_name":"user",
            "username": "testuser",
            "password": "securepassword",
            "password2": "securepassword",
            "gender": "Male",
            "phonenumber_primary": 1234567890,
            "phonenumber_secondary":0,
            "user_type": {
                "is_customer": True,
                "is_vendor": False
            }
        }
        response = client.post('/api/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class CustomerLoginTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )

    def test_customer_login(self):
        client = APIClient()
        data = {
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }
        response = client.post('/api/login/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class CustomerLogoutTest(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )

    def test_customer_logout(self):
        client = APIClient()
        # Log in the user first
        client.login(username='testuser', password='testpassword')
        response = client.post('/api/logout/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class CustomerDeleteAccountTest(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )

    def test_customer_delete_account(self):
        client = APIClient()
        # Log in the user first
        client.login(username='testuser', password='testpassword')
        response = client.delete('/api/delete-account/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

