"""Test module: Hosts."""
from django.test import TestCase
from django.contrib.auth.models import User, Group

from hubuum.models import Host


class HostTestCase(TestCase):
    """This class defines the test suite for the Host model."""

    #    def setUp(self):
    #        """Define the host object."""
    #        self.host_target = Host.objects.create(name='nommo', serial="42")

    def setUp(self):
        """Set up defaults for the test object."""
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
        """Try to create a host object owned by the test group."""
        host = Host.objects.create(
            name=self.hostname, serial=self.serial, owner=self.group
        )
        self.assertIsNotNone(host)
        self.assertIsInstance(host, Host)

    def test_create_has_correct_values(self):
        """Check that a created Host object returns the same values we fed it."""
        host = Host.objects.create(
            name=self.hostname, serial=self.serial, owner=self.group
        )
        self.assertEqual(host.serial, self.serial)
        self.assertEqual(host.name, self.hostname)
