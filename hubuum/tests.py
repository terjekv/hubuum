from django.test import TestCase
from django.contrib.auth.models import User, Group

from .models import Host

# Create your tests here.


class UserAndGroupTestCase(TestCase):
    """This class defines the test suite for the User and Group models."""

    def setUp(self) -> None:
        self.username = "tester"
        self.password = "testpassword"

        self.groupname = "testgroup"

    def test_can_create_user(self):
        self.user = User.objects.create(username=self.username, password=self.password)
        self.assertIsNotNone(self.user)

    def test_can_create_group(self):
        self.group = Group.objects.create(name=self.groupname)
        self.assertIsNotNone(self.group)

    def test_can_assign_group_to_user(self):
        self.user = User.objects.create(username=self.username, password=self.password)
        self.assertIsNotNone(self.user)
        self.group = Group.objects.create(name=self.groupname)
        self.assertIsNotNone(self.group)
        self.user.groups.set([self.group])
        self.assertEqual(self.user.groups.all()[0].name, self.groupname)
        self.assertCountEqual(self.user.groups.all(), [self.group])


# login = self.client.login(username="testuser", password="12345")


class HostTestCase(TestCase):
    """This class defines the test suite for the Host model."""

    #    def setUp(self):
    #        """Define the host object."""
    #        self.host_target = Host.objects.create(name='nommo', serial="42")

    def setUp(self):
        self.hostname = "testhost"
        self.serial = "test_serial_1"
        self.username = "tester"
        self.password = "testpassword"
        self.groupname = "testgroup"

        self.user = User.objects.create(username=self.username, password=self.password)
        self.assertIsNotNone(self.user)

        self.group = Group.objects.create(name=self.groupname)
        self.assertIsNotNone(self.group)

    def test_can_create_host(self):
        host = Host.objects.create(
            name=self.hostname, serial=self.serial, owner=self.group
        )
        self.assertIsNotNone(host)
        self.assertIsInstance(host, Host)

    def test_create_has_correct_values(self):
        host = Host.objects.create(
            name=self.hostname, serial=self.serial, owner=self.group
        )
        self.assertEqual(host.serial, self.serial)
        self.assertEqual(host.name, self.hostname)
