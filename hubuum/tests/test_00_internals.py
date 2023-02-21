"""Test module: Users and Groups."""
import pytest
from rest_framework.exceptions import NotFound

from hubuum.exceptions import MissingParam
from hubuum.models import Namespace, User
from hubuum.tools import get_object

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
            self._test_has_identical_values(obj=self.user)
        with pytest.raises(MissingParam):
            self._test_has_identical_values(dictionary={})

    # Using assert triggers bandit:
    # https://bandit.readthedocs.io/en/latest/plugins/b101_assert_used.html
    # However, producing a consistent configuration across workflows and
    # external tools is proving annoying, so we mark out the lines directly.
    def test_get_object(self):
        """Test the get_object interface from tools."""
        assert isinstance(get_object(User, "test"), User) is True  # nosec
        assert get_object(User, "doesnotexist", raise_exception=False) is None  # nosec
        with pytest.raises(NotFound):
            assert get_object(User, "doesnotexist")  # nosec

    def test_has_perm(self):
        """Test the internals of has_perm."""
        # These should never happen, but are handled.
        test = User.objects.get(username="test")
        assert test.has_perm("hubuum.read_namespace", None) is False  # nosec
        with pytest.raises(MissingParam):
            test.has_perm("nosuchperm", None)
        with pytest.raises(MissingParam):
            test.has_perm("hubuum.x_y", None)
        with pytest.raises(MissingParam):
            test.has_perm("hubuum.nosuchperm_host", None)
        with pytest.raises(MissingParam):
            test.has_perm("hubuum.read_nosuchmodel", None)
        with pytest.raises(MissingParam):
            test.namespaced_can("nosuchperm", None)

        Namespace.objects.get_or_create(name="root")
        assert test.can_modify_namespace("root") is False  # nosec
        with pytest.raises(NotFound):
            test.can_modify_namespace("root.no")
        with pytest.raises(NotFound):
            test.can_modify_namespace("root.no.reallyno")
