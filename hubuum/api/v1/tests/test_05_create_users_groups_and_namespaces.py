"""Test users, groups, and namespaces."""

from .base import HubuumAPIBaseTestCase


class APIUsersAndGroupsTestCase(HubuumAPIBaseTestCase):
    """Test creating users and groups operations."""

    def test_staff_create_user(self):
        """Test authenticated user creation."""
        self.client = self.get_staff_client()
        response = self.assert_post(
            "/users/", {"username": "userone", "password": "test"}
        )
        self.assertEqual(response.data["username"], "userone")

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

    def test_create_and_delete_group(self):
        """Test authenticated group creation."""
        self.client = self.get_staff_client()
        response = self.assert_post("/groups/", {"name": "groupone"})
        self.assertEqual(response.data["name"], "groupone")
        response = self.assert_get("/groups/")
        self.assertEqual(len(response.data), 1)

        self.assert_delete("/group/" + str(response.data[0]["id"]))
        response = self.assert_get("/groups/")
        self.assertEqual(len(response.data), 0)

        # Repeat the same for a normal user. This implicitly creates another group...
        self.client = self.get_user_client()
        response = self.assert_get("/groups/")
        self.assertEqual(len(response.data), 1)

        self.assert_delete_and_403("/group/" + str(response.data[0]["id"]))
        response = self.assert_get("/groups/")
        self.assertEqual(len(response.data), 1)

    def test_staff_add_user_to_group(self):
        """Test add user to group."""
        self.client = self.get_staff_client()
        self.assert_post(
            "/users/",
            {"username": "userone", "password": "test", "email": "test@test.nowhere"},
        )
        userresponse = self.assert_get("/user/userone")
        self.assertEqual(userresponse.data["username"], "userone")
        self.assertEqual(len(userresponse.data["groups"]), 0)
        groupresponse = self.assert_post("/groups/", {"name": "groupone"})
        self.assertEqual(groupresponse.data["name"], "groupone")

        self.assert_patch("/user/userone", {"groups": [groupresponse.data["id"]]})
        userresponse = self.assert_get("/user/userone")
        self.assertEqual(userresponse.data["username"], "userone")
        self.assertEqual(len(userresponse.data["groups"]), 1)

    def test_user_create_group(self):
        """Test normal users ability to create groups."""
        self.client = self.get_user_client()
        self.assert_post_and_403("/groups/", {"name": "groupone"})

    def test_patch_group(self):
        """Test normal users ability to patch groups."""
        self.client = self.get_staff_client()
        self.assert_post("/groups/", {"name": "groupone"})
        self.assert_patch_and_400("/group/groupone", {"wrongkey": "nope"})

        self.client = self.get_user_client()
        self.assert_get("/group/groupone")
        self.assert_patch_and_403("/group/groupone", {"name": "nope"})

    def test_user_delete_group(self):
        """Test normal users ability to delete groups."""
        self.client = self.get_user_client()
        self.assert_delete_and_403("/group/0")


class APINamespaceTestCase(HubuumAPIBaseTestCase):
    """Test creation and manipulation of Namespaces."""

    def test_staff_create_namespace(self):
        """Test authenticated namespace creation."""
        self.client = self.get_staff_client()
        response = self.assert_post("/namespaces/", {"name": "namespaceone"})
        self.assertEqual(response.data["name"], "namespaceone")
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
