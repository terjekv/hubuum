"""Test module: Users and Groups."""
from django.test import TestCase
from django.contrib.auth.models import User, Group


class UserAndGroupTestCase(TestCase):
    """This class defines the test suite for the User and Group models."""

    def setUp(self) -> None:
        """Set up defaults for the test object."""
        self.username = "tester"
        self.password = "testpassword"

        self.groupname = "testgroup"

    def test_can_create_user(self):
        """Try to create a user."""
        self.user = User.objects.create(username=self.username, password=self.password)
        self.assertIsNotNone(self.user)

    def test_can_create_group(self):
        """Try to create a group."""
        self.group = Group.objects.create(name=self.groupname)
        self.assertIsNotNone(self.group)

    def test_can_assign_group_to_user(self):
        """Try to make a user a member of a group."""
        self.user = User.objects.create(username=self.username, password=self.password)
        self.assertIsNotNone(self.user)
        self.group = Group.objects.create(name=self.groupname)
        self.assertIsNotNone(self.group)
        self.user.groups.set([self.group])
        self.assertEqual(self.user.groups.all()[0].name, self.groupname)
        self.assertCountEqual(self.user.groups.all(), [self.group])


# login = self.client.login(username="testuser", password="12345")
