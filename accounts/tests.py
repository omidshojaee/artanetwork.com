from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.test import TestCase

# Create your tests here.

User = get_user_model()


class UserManagerTests(TestCase):

    def test_create_user_with_email_successful(self):
        email = 'test@example.com'
        password = 'testpassword123'
        user = User.objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_user_without_email_raises_error(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email=None, password='testpassword123')

    def test_create_superuser_successful(self):
        email = 'admin@example.com'
        password = 'adminpassword123'
        superuser = User.objects.create_superuser(email=email, password=password)

        self.assertEqual(superuser.email, email)
        self.assertTrue(superuser.check_password(password))
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_create_superuser_with_is_staff_false_raises_error(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='admin@example.com', password='adminpassword123', is_staff=False
            )

    def test_create_superuser_with_is_superuser_false_raises_error(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='admin@example.com',
                password='adminpassword123',
                is_superuser=False,
            )


class UserModelTests(TestCase):

    def test_user_email_normalized(self):
        email = 'Test@EXAMPLE.com'
        user = User.objects.create_user(email=email, password='testpassword123')
        self.assertEqual(user.email, 'test@example.com')

    def test_user_email_unique(self):
        email = 'unique@example.com'
        User.objects.create_user(email=email, password='testpassword123')
        with self.assertRaises(IntegrityError):
            User.objects.create_user(email=email, password='testpassword123')

    def test_username_field_is_none(self):
        email = 'test@example.com'
        user = User.objects.create_user(email=email, password='testpassword123')
        self.assertIsNone(user.username)

    def test_user_has_date_joined(self):
        email = 'test@example.com'
        user = User.objects.create_user(email=email, password='testpassword123')
        self.assertIsNotNone(user.date_joined)

    def test_user_has_last_login_field(self):
        email = 'test@example.com'
        user = User.objects.create_user(email=email, password='testpassword123')
        self.assertIsNone(user.last_login)

    def test_user_meta_verbose_name(self):
        self.assertEqual(User._meta.verbose_name, 'user')

    def test_user_meta_verbose_name_plural(self):
        self.assertEqual(User._meta.verbose_name_plural, 'users')
