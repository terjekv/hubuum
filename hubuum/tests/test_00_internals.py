"""Test module: Users and Groups."""
from django.test import TestCase
import pytest

from hubuum.exceptions import MissingParam


class InternalsTestCase(TestCase):
    """This class defines the test suite for internal structures."""

    def test_exception_missing_param(self):
        """Test the MissingParam exception."""
        with pytest.raises(MissingParam):
            self._missing_param()

    def _missing_param(self, not_provided=None):
        """Raise an exception when not_provided lacks a value."""
        if not_provided is None:
            raise MissingParam
