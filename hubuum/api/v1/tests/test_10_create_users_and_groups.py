"""Test authentication."""

from .base import HubuumAPITestCase


class APIUsersAndGroupsTestCase(HubuumAPITestCase):
    """Test creating users and groups operations."""

    def test_staff_create_user(self):
        """Test authenticated user creation."""
        self.client = self.get_staff_client()
        response = self.assert_post(
            "/users/", {"username": "userone", "password": "test"}
        )
        data = response.json()
        self.assertEqual(data["username"], "userone")

    def test_user_create_user(self):
        """Test normal users ability to create users."""
        self.client = self.get_user_client()
        self.assert_post_and_403("/users/", {"username": "userone", "password": "test"})

    def test_list_users(self):
        """Test listing of users."""
        self.client = self.get_staff_client()
        # We currently have two users created during setUp()
        response = self.assert_get("/users/")
        self.assertEqual(len(response.data), 2)

    # TODO: #30 Also test by email.
    def test_get_user_by_username(self):
        """Test getting of users by username."""
        self.client = self.get_staff_client()
        # We currently have two users created during setUp()
        response = self.assert_get("/user/superuser")
        self.assertEqual(response.data["username"], "superuser")
        self.assert_get_and_404("/user/nosuchusername")

    def test_staff_create_group(self):
        """Test authenticated group creation."""
        self.client = self.get_staff_client()
        response = self.assert_post("/groups/", {"name": "groupone"})
        data = response.json()
        self.assertEqual(data["name"], "groupone")

    def test_user_create_group(self):
        """Test normal users ability to create groups."""
        self.client = self.get_user_client()
        self.assert_post_and_403("/groups/", {"name": "groupone"})
