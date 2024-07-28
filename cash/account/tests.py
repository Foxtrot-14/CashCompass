from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User
from django.contrib.auth.hashers import make_password
class UserAPITests(APITestCase):

    def setUp(self):
        self.registration_url = reverse('user_registration')  
        self.login_url = reverse('user_login')               
        self.user_detail_url = lambda pk: reverse('user_detail', args=[pk])  
        self.user_data = {
            'phone': '1234567890',
            'email': 'test@example.com',
            'name': 'Test User',
            'password1': 'password123',
            'password2': 'password123',
        }
        
        self.user_login_data = {
            'identifier': 'test@example.com',
            'password': 'password123',
        }

    def test_registration_success(self):
        response = self.client.post(self.registration_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('tokens', response.data)

    def test_registration_missing_fields(self):
        incomplete_data = self.user_data.copy()
        del incomplete_data['email']  # Remove email to test missing field
        response = self.client.post(self.registration_url, incomplete_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Missing fields', response.data['error'])

    def test_registration_passwords_mismatch(self):
        self.user_data['password2'] = 'differentpassword'
        response = self.client.post(self.registration_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Passwords do not match')

    def test_login_success(self):
        self.client.post(self.registration_url, self.user_data, format='json')  # Register the user first
        response = self.client.post(self.login_url, self.user_login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tokens', response.data)

    def test_login_user_not_found(self):
        invalid_login_data = {
            'identifier': 'nonexistent@example.com',
            'password': 'somepassword',
        }
        response = self.client.post(self.login_url, invalid_login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'User not found')

    def test_login_invalid_credentials(self):
        self.client.post(self.registration_url, self.user_data, format='json')  # Register the user first
        invalid_login_data = {
            'identifier': 'test@example.com',
            'password': 'wrongpassword',
        }
        response = self.client.post(self.login_url, invalid_login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['error'], 'Invalid credentials')

    def test_user_detail_get(self):
        response = self.client.post(self.registration_url, self.user_data, format='json')
        tokens = response.data['tokens']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + tokens['access'])  # Authenticate user

        user = User.objects.get(email=self.user_data['email'])
        response = self.client.get(self.user_detail_url(user.id), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user', response.data)

    def test_user_detail_patch(self):
        response = self.client.post(self.registration_url, self.user_data, format='json')
        tokens = response.data['tokens']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + tokens['access'])  # Authenticate user

        user = User.objects.get(email=self.user_data['email'])
        update_data = {
            'name': 'Updated Name'
        }
        response = self.client.patch(self.user_detail_url(user.id), update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['name'], 'Updated Name')

    def test_user_detail_patch_unauthorized(self):
        response = self.client.post(self.registration_url, self.user_data, format='json')
        tokens = response.data['tokens']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + tokens['access']) 
        another_user = User.objects.create(
            phone='0987654321',
            email='another@example.com',
            name='Another User',
            password=make_password('password123')
        )
        update_data = {
            'name': 'Unauthorized Update'
        }
        response = self.client.patch(self.user_detail_url(another_user.id), update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['error'], 'You are not authorized to make changes')
