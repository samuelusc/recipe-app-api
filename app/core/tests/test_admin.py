"""
Tests for the Django admin modifications.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTests(TestCase):
    """Tests for the Django admin site."""

    def setUp(self):
        """Create user and client for testing."""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='passtest123',
        )
        # force login the admin user
        self.client.force_login(self.admin_user)
        # create a regular user
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='passtest123',
            name='Test User',
        )

    def test_users_listed(self):
        # Test that users are listed on the user page.
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    # Test that the user edit page works.
    def test_user_change_page(self):
        """Test that the user edit page works."""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that the create user page works."""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
