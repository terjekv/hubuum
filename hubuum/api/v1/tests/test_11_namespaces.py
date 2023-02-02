"""Test namespaces."""
from .base import HubuumAPITestCase


class APINamespace(HubuumAPITestCase):
    """Test namespaces."""

    def test_readonly_fields(self):
        """Test that we can't write to read-only fields."""
        self.assert_post("/namespaces/", {"name": "namespaceone"})
        self.assert_patch_and_400(
            "/namespaces/namespaceone", {"created_at", "2022-01-01"}
        )

    def test_namespaces_as_superuser(self):
        """Test namespaces as a superuser."""
        self.client = self.get_superuser_client()

        self.assert_post("/namespaces/", {"name": "namespaceone"})
        self.assert_post_and_400("/namespaces/", {"name": "namespaceone"})
        self.assert_get("/namespaces/namespaceone")

        self.assert_get_elements("/namespaces/", 1)
        self.assert_post("/namespaces/", {"name": "namespacetwo"})
        self.assert_get_elements("/namespaces/", 2)
        self.assert_delete("/namespaces/namespaceone")
        self.assert_get_elements("/namespaces/", 1)
        self.assert_delete_and_404("/namespaces/namespaceone")

        response = self.assert_get_elements("/namespaces/", 1)
        nid = response.data[0]["id"]
        self.assert_patch(f"/namespaces/{nid}", {"name": "namespace_not_two"})
        self.assert_get("/namespaces/namespace_not_two")
        self.assert_get(f"/namespaces/{nid}")
        self.assert_delete(f"/namespaces/{nid}")
        self.assert_get_elements("/namespaces/", 0)
        self.assert_get_and_404("/namespaces/namespace_not_two")

    def test_namespaces_as_user(self):
        """Test namespaces as a normal user."""
        self.client = self.get_user_client()

        self.assert_get_elements("/namespaces/", 0)
        self.assert_post_and_403("/namespaces/", {"name": "namespaceone"})
        self.assert_get_elements("/namespaces/", 0)

        self.client = self.get_superuser_client()
        self.assert_post("/namespaces/", {"name": "namespaceone"})

        self.assert_post("/users/", {"username": "tmpuser", "password": "test"})
        self.assert_post("/groups/", {"name": "tmpgroup"})

        self.assert_post("/groups/tmpgroup/members/tmpuser")
        self.assert_get("/users/tmpuser")

        self.client = self.get_user_client(username="tmp")
