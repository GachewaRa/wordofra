from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
import json

from .models import NewsletterSubscriber, Profile

User = get_user_model()


class AuthenticationTests(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('customuser-list')
        self.login_url = reverse('jwt-create')
        self.custom_login_url = reverse('custom-login')
        self.user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'TestPass123',
            # 're_password': 'TestPass123',
            'first_name': 'Test',
            'last_name': 'User',
        }

    def test_user_registration(self):
        """Test user registration with Djoser."""
        response = self.client.post(self.register_url, self.user_data)
        # print(f"Response data: {response.data}") 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'test@example.com')
        
        # Verify profile was created
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(Profile.objects.get().user.email, 'test@example.com')

    def test_user_login(self):
        """Test user login with Djoser JWT."""
        # Create user first
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='TestPass123',
            first_name='Test',
            last_name='User'
        )
        
        # Login
        login_data = {
            'email': 'test@example.com',
            'password': 'TestPass123'
        }
        response = self.client.post(self.login_url, login_data)
        # print("RESPONSE DATA: ", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_custom_login_with_lockout(self):
        """Test custom login view with account lockout functionality."""
        # Create user
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='TestPass123',
            first_name='Test',
            last_name='User'
        )
        
        # Attempt login with incorrect password 5 times
        incorrect_login = {
            'email': 'test@example.com',
            'password': 'WrongPassword'
        }
        
        for i in range(5):
            response = self.client.post(self.custom_login_url, incorrect_login)
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
            # Refresh user data after each attempt to see changes
            self.user.refresh_from_db()
            # print(f"After attempt {i+1}: failed_login_attempts={self.user.failed_login_attempts}")
        
        # Verify account is now locked
        self.user.refresh_from_db()
        # print(f"Final failed_login_attempts after test: {self.user.failed_login_attempts}")
        self.assertEqual(self.user.failed_login_attempts, 5)
        self.assertIsNotNone(self.user.last_failed_login)

    def test_password_change(self):
        """Test password change with Djoser."""
        # Create and authenticate user
        user = User.objects.create_user(
            email='newuser@example.com',
            username='newuser',
            password='TestPass123',
            first_name='Test',
            last_name='User'
        )
        # Get tokens
        login_data = {
            'email': 'newuser@example.com',
            'password': 'TestPass123'
        }
        response = self.client.post(self.login_url, login_data)
        token = response.data['access']
        
        # Change password
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {token}')
        password_change_url = reverse('customuser-set-password')
        password_data = {
            'current_password': 'TestPass123',
            'email': 'newuser@example.com',
            'new_password': 'NewPassword456'
        }
        response = self.client.post(password_change_url, password_data)
        # print(f"Password change response: {response.status_code}, {response.data}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Try logging in with new password
        self.client.credentials() # Clear auth
        login_data = {
            'email': 'newuser@example.com',
            'password': 'NewPassword456'
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_update(self):
        """Test updating user details with Djoser."""
        # Create and authenticate user
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='TestPass123',
            first_name='Test',
            last_name='User'
        )
        
        # Get tokens
        login_data = {
            'email': 'test@example.com',
            'password': 'TestPass123'
        }
        response = self.client.post(self.login_url, login_data)
        token = response.data['access']
        
        # Update user
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {token}')
        me_url = reverse('customuser-me')
        update_data = {
            'first_name': 'Updated',
            'last_name': 'Name'
        }
        
        response = self.client.patch(me_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify changes
        user.refresh_from_db()
        self.assertEqual(user.first_name, 'Updated')
        self.assertEqual(user.last_name, 'Name')


class NewsletterTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.subscribe_url = reverse('newsletter-subscribe')
        self.opt_in_url = reverse('newsletter-opt-in')
        self.unsubscribe_url = reverse('newsletter-unsubscribe')
        self.user_unsubscribe_url = reverse('user-newsletter-unsubscribe')
        
        # Create a user
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='TestPass123',
            first_name='Test',
            last_name='User'
        )
        
    def test_anonymous_subscription(self):
        """Test newsletter subscription for anonymous users."""
        data = {
            'email': 'subscriber@example.com',
            'name': 'New Subscriber'
        }
        
        response = self.client.post(self.subscribe_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(NewsletterSubscriber.objects.count(), 1)
        subscriber = NewsletterSubscriber.objects.first()
        self.assertEqual(subscriber.email, 'subscriber@example.com')
        self.assertEqual(subscriber.name, 'New Subscriber')
    
    def test_user_opt_in(self):
        """Test newsletter opt-in for authenticated users."""
        # Login
        login_url = reverse('jwt-create')
        login_data = {
            'email': 'test@example.com',
            'password': 'TestPass123'
        }
        response = self.client.post(login_url, login_data)
        token = response.data['access']
        
        # Opt in to newsletter
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {token}')
        response = self.client.post(self.opt_in_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify user is subscribed
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_newsletter_subscribed)
        
        # Verify entry was created in NewsletterSubscriber
        self.assertEqual(NewsletterSubscriber.objects.count(), 1)
        subscriber = NewsletterSubscriber.objects.first()
        self.assertEqual(subscriber.email, 'test@example.com')
    
    def test_anonymous_unsubscribe(self):
        """Test newsletter unsubscription for anonymous users."""
        # Create subscriber first
        subscriber = NewsletterSubscriber.objects.create(
            email='subscriber@example.com',
            name='Subscriber'
        )
        
        # Unsubscribe
        data = {
            'email': 'subscriber@example.com'
        }
        response = self.client.post(self.unsubscribe_url, data)
        # print(f"Anonymous Unsubscribe response: {response.status_code}, {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify deletion
        self.assertEqual(NewsletterSubscriber.objects.count(), 0)
    
    def test_user_unsubscribe(self):
        """Test newsletter unsubscription for authenticated users."""
        # First opt in
        self.user.is_newsletter_subscribed = True
        self.user.save()
        subscriber = NewsletterSubscriber.objects.create(
            email='test@example.com'
        )
        
        # Login
        login_url = reverse('jwt-create')
        login_data = {
            'email': 'test@example.com',
            'password': 'TestPass123'
        }
        response = self.client.post(login_url, login_data)
        token = response.data['access']
        
        # Unsubscribe
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {token}')
        response = self.client.post(self.user_unsubscribe_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify user is unsubscribed
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_newsletter_subscribed)
        
        # Verify entry was deleted from NewsletterSubscriber
        self.assertEqual(NewsletterSubscriber.objects.count(), 0)
    

class UserAccountDeletionTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='TestPass123',
            first_name='Test',
            last_name='User'
        )
        
    def test_account_deletion(self):
        """Test user account deletion with Djoser."""
        # Login
        login_url = reverse('jwt-create')
        login_data = {'email': 'test@example.com', 'password': 'TestPass123'}
        response = self.client.post(login_url, login_data)
        token = response.data['access']
        
        # Delete account
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {token}')
        delete_url = reverse('customuser-me')
        delete_data = {"current_password": "TestPass123"}  
        delete_response = self.client.delete(
            delete_url,
            data=json.dumps(delete_data),  # Convert to JSON
            content_type='application/json'
        )
        
        # print(f"User account response: {delete_response.status_code}, {delete_response.data}")
        
        # Check if user is actually deleted
        user_exists = User.objects.filter(email='test@example.com').exists()
        # print(f"User exists after deletion? {user_exists}")
        
        # Fix assertion: Djoser may return 200 instead of 204
        self.assertIn(delete_response.status_code, [200, 204])

        # Verify user and profile deletion
        self.assertFalse(User.objects.filter(email='test@example.com').exists())
        self.assertFalse(Profile.objects.exists())  # If Profile is related via cascade


# Fixtures for easier testing
# class FixturesTest(TestCase):
#     def test_create_fixtures(self):
#         """
#         This is not a real test but a convenient way to generate fixtures.
#         Run this test to create initial data for manual testing.
#         """
#         # Create sample users
#         users = [
#             {
#                 'email': 'admin@example.com',
#                 'username': 'admin',
#                 'password': 'AdminPass123',
#                 'first_name': 'Admin',
#                 'last_name': 'User',
#                 'is_staff': True,
#                 'is_superuser': True
#             },
#             {
#                 'email': 'user1@example.com',
#                 'username': 'user1',
#                 'password': 'UserPass123',
#                 'first_name': 'Regular',
#                 'last_name': 'User',
#             },
#             {
#                 'email': 'subscriber@example.com',
#                 'username': 'subscriber',
#                 'password': 'SubPass123',
#                 'first_name': 'Newsletter',
#                 'last_name': 'Subscriber',
#                 'is_newsletter_subscribed': True
#             }
#         ]
        
#         for user_data in users:
#             is_staff = user_data.pop('is_staff', False)
#             is_superuser = user_data.pop('is_superuser', False)
#             is_newsletter = user_data.pop('is_newsletter_subscribed', False)
#             password = user_data.pop('password')
            
#             user = User.objects.create_user(**user_data)
#             user.set_password(password)
#             user.is_staff = is_staff
#             user.is_superuser = is_superuser
#             user.is_newsletter_subscribed = is_newsletter
#             user.save()
            
#             if is_newsletter:
#                 NewsletterSubscriber.objects.create(email=user.email)
        
#         # Create anonymous subscribers
#         subscribers = [
#             {'email': 'anon1@example.com', 'name': 'Anonymous One'},
#             {'email': 'anon2@example.com', 'name': 'Anonymous Two'},
#         ]
        
#         for sub_data in subscribers:
#             NewsletterSubscriber.objects.create(**sub_data)
            
#         print("Fixtures created successfully!")
#         # This will always pass - it's just for generating test data
#         self.assertTrue(True)