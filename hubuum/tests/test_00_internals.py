"""Test module: Users and Groups."""
import pytest

from hubuum.exceptions import MissingParam

from .base import HubuumModelTestCase


class InternalsTestCase(HubuumModelTestCase):
    """This class defines the test suite for internal structures."""

    def test_exception_missing_param(self):
        """Test the MissingParam exception."""
        # _create_object requires kwarg model.
        with pytest.raises(MissingParam):
            self._create_object()

        # _test_has_identical_values requires kwargs dictionary and object
        with pytest.raises(MissingParam):
            self._test_has_identical_values()
        with pytest.raises(MissingParam):
            self._test_has_identical_values(object=self.user)
        with pytest.raises(MissingParam):
            self._test_has_identical_values(dictionary={})
