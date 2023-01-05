from django.test import TestCase

from .models import Host

# Create your tests here.


class HostTestCase(TestCase):
    """This class defines the test suite for the Host model."""

    #    def setUp(self):
    #        """Define the host object."""
    #        self.host_target = Host.objects.create(name='nommo', serial="42")

    def setUp(self):
        self.hostname = "testhost"
        self.serial = "test_serial_1"

    def test_can_create_host(self):
        host = Host.objects.create(name=self.hostname, serial=self.serial)
        self.assertIsNotNone(host)
        self.assertIsInstance(host, Host)

    def test_create_has_correct_values(self):
        host = Host.objects.create(name=self.hostname, serial=self.serial)
        self.assertEqual(host.serial, self.serial)
        self.assertEqual(host.name, self.hostname)
