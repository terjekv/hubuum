"""Test users, groups, and namespaces."""

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

        # Repeat the same for a normal user. This implicitly creates another user.
        self.client = self.get_user_client()
        response = self.assert_get("/users/")
        self.assertEqual(len(response.data), 3)

    def test_get_user_by_username_or_email(self):
        """Test getting of users by username or email."""
        self.client = self.get_staff_client()
        self.assert_post(
            "/users/",
            {"username": "userone", "password": "test", "email": "test@test.nowhere"},
        )
        response = self.assert_get("/user/userone")
        self.assertEqual(response.data["username"], "userone")
        response = self.assert_get("/user/test@test.nowhere")
        self.assertEqual(response.data["username"], "userone")
        self.assert_get_and_404("/user/nosuchusername")

    def test_staff_create_group(self):
        """Test authenticated group creation."""
        self.client = self.get_staff_client()
        response = self.assert_post("/groups/", {"name": "groupone"})
        data = response.json()
        self.assertEqual(data["name"], "groupone")
        response = self.assert_get("/groups/")
        self.assertEqual(len(response.data), 1)

        # Repeat the same for a normal user. This implicitly creates another group...
        self.client = self.get_user_client()
        response = self.assert_get("/groups/")
        self.assertEqual(len(response.data), 2)

    def test_user_create_group(self):
        """Test normal users ability to create groups."""
        self.client = self.get_user_client()
        self.assert_post_and_403("/groups/", {"name": "groupone"})


class APINamespaceTestCase(HubuumAPITestCase):
    """Test creation and manipulation of Namespaces."""

    def test_staff_create_namespace(self):
        """Test authenticated namespace creation."""
        self.client = self.get_staff_client()
        response = self.assert_post("/namespaces/", {"name": "namespaceone"})
        data = response.json()
        self.assertEqual(data["name"], "namespaceone")
        self.assert_get_and_200("/namespace/namespaceone")

    def test_user_create_root_namespace(self):
        """Test users ability to create root namespaces."""
        self.client = self.get_user_client()
        self.assert_post_and_403("/namespaces/", {"name": "namespaceone"})

    def test_user_create_scoped_namespace(self):
        """Test users ability to create root namespaces."""
        self.client = self.get_user_client()
        self.assert_post_and_403("/namespaces/", {"name": "namespaceone.mine"})

        # Test giving the user access and create a scoped namespace
