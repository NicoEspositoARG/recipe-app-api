from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def create_user(email='test@somemail.com', password='testpass'):
    """Create sample user"""
    return get_user_model().objects.create_user(email, password)


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

    def test__email_normalized(self):
        """Test the email for a new user is normalized"""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.com', 'test4@example.com'],
        ]
        for email, expected in sample_emails:

            user = get_user_model().objects.create_user(
                email=email,
                password='test1233'
            )
        self.assertEqual(user.email, expected)

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

    def test_tag_str(self):
        "Test the tag string representation"
        tag = models.Tag.objects.create(
            user=create_user(),
            name='Vegan'
        )
        self.assertEqual(str(tag), tag.name)

    def test_create_tag(self):
        """Test creating a tag is successful."""
        user = create_user()
        tag = models.Tag.objects.create(user=user, name='Tag1')
        self.assertEqual(str(tag), tag.name)

    def test_create_recipe(self):
        """Test creating a recipe is successful."""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'pass123',
        )
        recipe = models.Recipe.objects.create(
            user=user,
            title='Sample recipe name',
            time_minutes=5,
            price=Decimal('5.50'),  # for financial apps, use integer instead!
            description='Sample recipe description',
        )

        self.assertEqual(str(recipe), recipe.title)

    def test_create_ingredient(self):
        """Test creating an ingredient is succesful."""
        user = create_user()
        ingredient = models.Ingredient.objects.create(
            user=user,
            name='Ingredient1'
        )
        self.assertEqual(str(ingredient), ingredient.name)
