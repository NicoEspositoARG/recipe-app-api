from django.test import TestCase
from django.contrib.auth import get_user_model


class Modeltests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is succesfull"""
        email = "test@sarasamail.com"
        password = "Testpass123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@SARAMAILCAPS.COM'
        user = get_user_model().objects.create_user(
            email=email,
            password='test1233'
        )
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            # if ValueError is not raised, the test fails.

            get_user_model().objects.create_user(
                email=None,
                password="Test123"
            )

    def test_create_new_super_user(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@sarasamail.com',
            'pass123'
        )
        self.assertTrue(user.is_superuser)
        # this prop superuser is included in the permission mixin of the model
        self.assertTrue(user.is_staff)
