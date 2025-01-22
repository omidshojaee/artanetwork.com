from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from django.utils import timezone

# Create your tests here.

User = get_user_model()


class TestUserManager(TestCase):
    def test_create_user(self):
        """Test creating a regular user"""
        user = User.objects.create_user(
            email='test@example.com', password='testpass123'
        )
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_create_user_without_email(self):
        """Test creating a user without email raises error"""
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password='testpass123')
        with self.assertRaises(ValueError):
            User.objects.create_user(email=None, password='testpass123')

    def test_create_superuser(self):
        """Test creating a superuser"""
        admin_user = User.objects.create_superuser(
            email='admin@example.com', password='testpass123'
        )
        self.assertEqual(admin_user.email, 'admin@example.com')
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_active)

    def test_create_superuser_with_invalid_flags(self):
        """Test creating superuser with invalid is_staff/is_superuser flags"""
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='admin@example.com', password='testpass123', is_staff=False
            )
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='admin@example.com', password='testpass123', is_superuser=False
            )

    def test_email_normalize(self):
        """Test email normalization"""
        email = 'test@EXAMPLE.com'
        user = User.objects.create_user(email=email, password='testpass123')
        self.assertEqual(user.email, email.lower())


class TestUserModel(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User',
        }

    def test_user_creation(self):
        """Test creating a user with valid data"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.first_name, self.user_data['first_name'])
        self.assertEqual(user.last_name, self.user_data['last_name'])

    def test_duplicate_email(self):
        """Test that duplicate emails are not allowed"""
        User.objects.create_user(**self.user_data)
        with self.assertRaises(IntegrityError):
            User.objects.create_user(**self.user_data)

    def test_email_max_length(self):
        """Test email max length validation"""
        email = 'a' * 245 + '@example.com'  # Total 254 characters
        user = User.objects.create_user(email=email, password='testpass123')
        self.assertEqual(user.email, email)

        # Email longer than 254 characters should raise validation error
        email = 'a' * 246 + '@example.com'  # Total 255 characters
        with self.assertRaises(ValidationError):
            user = User(email=email, password='testpass123')
            user.full_clean()

    def test_date_fields(self):
        """Test date_joined and last_login fields"""
        user = User.objects.create_user(**self.user_data)

        # Test date_joined is set automatically
        self.assertIsNotNone(user.date_joined)
        self.assertIsInstance(user.date_joined, timezone.datetime)

        # Test last_login is initially None
        self.assertIsNone(user.last_login)

    def test_username_field(self):
        """Test that username field is not used for authentication"""
        user = User.objects.create_user(**self.user_data)
        self.assertIsNone(user.username)  # Check that username is None
        self.assertEqual(
            User.USERNAME_FIELD, 'email'
        )  # Verify email is used for authentication

    def test_required_fields(self):
        """Test REQUIRED_FIELDS is empty and USERNAME_FIELD is email"""
        self.assertEqual(User.REQUIRED_FIELDS, [])
        self.assertEqual(User.USERNAME_FIELD, 'email')
