"""Test module for the Person model."""

from .base import HubuumModelTestCase

from hubuum.models import Person


class PersonTestCase(HubuumModelTestCase):
    """This class defines the test suite for the Person model."""

    def setUp(self):
        """Set up defaults for the test object."""
        super().setUp()
        self.attributes = {"username": "octocat", "email": "octocat@github.com"}
        self.object = self._test_can_create_object(model=Person, **self.attributes)

    def test_create_has_correct_values(self):
        """Check that a created object returns the same values we fed it (only name for now)."""
        self._test_has_identical_values(object=self.object, dictionary=self.attributes)

    def test_str(self):
        """Test that stringifying objects works as expected."""
        self._test_str()
