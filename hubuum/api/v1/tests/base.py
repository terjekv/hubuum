"""Provide a base class for testing."""

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from rest_framework.test import APIClient, APITestCase

from knox.models import AuthToken

from hubuum.models import Host


class MissingParam(Exception):
    """An exception thrown when a parameter is missing."""

    pass


# This testsuite design is based on the testsuite for MREG:
# https://github.com/unioslo/mreg/blob/master/mreg/api/v1/tests/tests.py
class HubuumAPITestCase(APITestCase):
    """Base APITestCase for the HubuumAPI (v1)."""

    def setUp(self):
        """By default setUp sets up an APIClient for the superuser with a token."""
        self.client = self.get_superuser_client()

    def get_superuser_client(self):
        """Get a client for the superuser."""
        return self._get_token_client(superuser=True)

    def get_adminuser_client(self):
        """Get a client for the adminuser."""
        return self._get_token_client(adminuser=True, superuser=False)

    def get_user_client(self, username="nobody", groupname="test_nobody_group"):
        """Get a client for a normal user.

        param: username (defaults to "nobody")
        param: groupname (defaults to "test_nobody_group")
        """
        return self._get_token_client(
            staff=False, superuser=False, username=username, groupname=groupname
        )

    def _get_token_client(
        self, username=None, groupname=None, superuser=True, staff=False
    ):
        """Create an APIClient with a token.

        Pass one of the following combinations:

        username=string, groupname=string (they will be created if they don't exist.)
        superuser=True (no superuser group will be created)
        staff=True (no staff group will be created)

        param: username (string, defaults to "None")
        param: groupname (string, defaults to "None")
        param: superuser (boolean, defaults to "True")
        param: staff (boolean, default to "False")
        """
        if username is None:
            if superuser:
                username = "superuser"
            elif staff:
                username = "adminuser"
            else:
                username = "nobody"

        self.user = get_user_model().objects.create_user(
            username=username, password="test"
        )
        self.user.groups.clear()

        if superuser:
            self.user.is_superuser = True
        elif staff:
            self.user.is_staff = True
        elif username == "nobody":
            self.add_user_to_groups("test_nobody_group")
        else:
            if not groupname:
                raise MissingParam

            self.add_user_to_groups(groupname)

        self.user.save()

        # https://github.com/James1345/django-rest-knox/blob/develop/knox/models.py
        token = AuthToken.objects.create(self.user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token " + token[1])
        return client

    def add_user_to_groups(self, groups):
        """Add a user to a group or a list of groups."""
        if not isinstance(groups, (list, tuple)):
            groups = (groups,)
        for groupname in groups:
            group, created = Group.objects.get_or_create(name=groupname)
            group.user_set.add(self.user)

    @staticmethod
    def _create_path(path):
        """Create a valid API path from the stub provided.

        Usage rules:

        1. If the parameter starts with /api/, use the param verbatim.
        2. If the parameter starts with /, remove the initial /, goto 2.
        3. Append the parameter to /api/v1/.

        parmams: path (string)
        """
        if path.startswith("/api/"):
            return path
        elif path.startswith("/"):
            return f"/api/v1/{path[1:]}"
        return f"/api/v1/{path}"

    def _assert_delete_and_status(self, path, status_code, client=None):
        """Delete and assert status."""
        if client is None:
            client = self.client
        response = client.delete(self._create_path(path))
        self.assertEqual(response.status_code, status_code)
        return response

    def _assert_get_and_status(self, path, status_code, client=None):
        """Get and assert status."""
        if client is None:
            client = self.client
        response = client.get(self._create_path(path))
        self.assertEqual(response.status_code, status_code)
        return response

    def _assert_patch_and_status(self, path, status_code, data=None, client=None):
        """Patch and assert status."""
        if client is None:
            client = self.client
        response = client.patch(self._create_path(path), data)
        self.assertEqual(response.status_code, status_code)
        return response

    def _assert_post_and_status(self, path, status_code, data=None, client=None):
        """Post and assert status."""
        if client is None:
            client = self.client
        response = client.post(self._create_path(path), data)
        self.assertEqual(response.status_code, status_code)
        return response

    def assert_delete(self, path, **kwargs):
        """Delete and assert status as 204."""
        return self.assert_delete_and_204(path, **kwargs)

    def assert_delete_and_204(self, path, **kwargs):
        """Delete and assert status as 204."""
        return self._assert_delete_and_status(path, 204, **kwargs)

    def assert_delete_and_403(self, path, **kwargs):
        """Delete and assert status as 403."""
        return self._assert_delete_and_status(path, 403, **kwargs)

    def assert_delete_and_404(self, path, **kwargs):
        """Delete and assert status as 404."""
        return self._assert_delete_and_status(path, 404, **kwargs)

    def assert_delete_and_409(self, path, **kwargs):
        """Delete and assert status as 409."""
        return self._assert_delete_and_status(path, 409, **kwargs)

    def assert_get(self, path, **kwargs):
        """Get and assert status as 200."""
        return self.assert_get_and_200(path, **kwargs)

    def assert_get_and_200(self, path, **kwargs):
        """Get and assert status as 200."""
        return self._assert_get_and_status(path, 200, **kwargs)

    def assert_get_and_400(self, path, **kwargs):
        """Get and assert status as 400."""
        return self._assert_get_and_status(path, 400, **kwargs)

    def assert_get_and_401(self, path, **kwargs):
        """Get and assert status as 401."""
        return self._assert_get_and_status(path, 401, **kwargs)

    def assert_get_and_404(self, path, **kwargs):
        """Get and assert status as 404."""
        return self._assert_get_and_status(path, 404, **kwargs)

    def assert_patch(self, path, *args, **kwargs):
        """Patch and assert status as 204."""
        return self.assert_patch_and_204(path, *args, **kwargs)

    def assert_patch_and_204(self, path, *args, **kwargs):
        """Patch and assert status as 204."""
        return self._assert_patch_and_status(path, 204, *args, **kwargs)

    def assert_patch_and_400(self, path, *args, **kwargs):
        """Patch and assert status as 400."""
        return self._assert_patch_and_status(path, 400, *args, **kwargs)

    def assert_patch_and_403(self, path, *args, **kwargs):
        """Patch and assert status as 204."""
        return self._assert_patch_and_status(path, 403, *args, **kwargs)

    def assert_patch_and_404(self, path, *args, **kwargs):
        """Patch and assert status as 404."""
        return self._assert_patch_and_status(path, 404, *args, **kwargs)

    def assert_patch_and_405(self, path, *args, **kwargs):
        """Patch and assert status as 405."""
        return self._assert_patch_and_status(path, 405, *args, **kwargs)

    def assert_patch_and_409(self, path, *args, **kwargs):
        """Patch and assert status as 409."""
        return self._assert_patch_and_status(path, 409, *args, **kwargs)

    def assert_post(self, path, *args, **kwargs):
        """Post and assert status as 201."""
        return self.assert_post_and_201(path, *args, **kwargs)

    def assert_post_and_200(self, path, *args, **kwargs):
        """Post and assert status as 200."""
        return self._assert_post_and_status(path, 200, *args, **kwargs)

    def assert_post_and_201(self, path, *args, **kwargs):
        """Post and assert status as 201."""
        return self._assert_post_and_status(path, 201, *args, **kwargs)

    def assert_post_and_204(self, path, *args, **kwargs):
        """Post and assert status as 204."""
        return self._assert_post_and_status(path, 204, *args, **kwargs)

    def assert_post_and_400(self, path, *args, **kwargs):
        """Post and assert status as 400."""
        return self._assert_post_and_status(path, 400, *args, **kwargs)

    def assert_post_and_401(self, path, *args, **kwargs):
        """Post and assert status as 401."""
        return self._assert_post_and_status(path, 401, *args, **kwargs)

    def assert_post_and_403(self, path, *args, **kwargs):
        """Post and assert status as 403."""
        return self._assert_post_and_status(path, 403, *args, **kwargs)

    def assert_post_and_404(self, path, *args, **kwargs):
        """Post and assert status as 404."""
        return self._assert_post_and_status(path, 404, *args, **kwargs)

    def assert_post_and_409(self, path, *args, **kwargs):
        """Post and assert status as 409."""
        return self._assert_post_and_status(path, 409, *args, **kwargs)


def clean_and_save(entity):
    """Perform a full clean and a save on the object.

    https://docs.djangoproject.com/en/4.1/ref/models/instances/#django.db.models.Model.full_clean
    """
    entity.full_clean()
    entity.save()


def create_host(name="testhost", ownergroup=None):
    """Create a host with an owner, directly against the model.

    params: name (defaults to "testhost")
    params: ownergroup (no default, group object expected, required)
    """
    if not ownergroup:
        raise MissingParam

    if not isinstance(ownergroup, Group):
        raise TypeError

    return Host.objects.create(name=name, owner=ownergroup)


# TODO: For every endpoint we should have and check input validation.