"""
Tests for models.
"""
from decimal import Decimal
from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def create_user(email='user@example.com', password='testpass123'):
    """Create a return a new user."""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'
        password = 'testpass123'

        # Creates a new user from the user model using the create_user
        # function of the UserManager
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_recipe(self):
        """Test creating a recipe is successful."""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )
        recipe = models.Recipe.objects.create(
            user=user,
            title='Sample recipe name',
            time_minutes=5,
            price=Decimal('5.50'),
            description='Sample receipe description.',
        )

        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        """Test creating a tag is successful."""
        user = create_user()
        tag = models.Tag.objects.create(user=user, name='Tag1')

        self.assertEqual(str(tag), tag.name)

    def test_create_ingredient(self):
        """Test creating an ingredient is successful."""
        user = create_user()
        ingredient = models.Ingredient.objects.create(
            user=user,
            name='Ingredient1'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    @patch('core.models.uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test generating image path."""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'example.jpg')

        self.assertEqual(file_path, f'uploads/recipe/{uuid}.jpg')
