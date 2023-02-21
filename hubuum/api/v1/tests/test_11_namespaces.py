"""Test namespaces."""
from .base import HubuumAPITestCase


class APINamespace(HubuumAPITestCase):
    """Test namespaces."""

    def test_field_validation(self):
        """Test that we can't write to read-only fields."""
        self.assert_post("/namespaces/", {"name": "namespaceone"})
        self.assert_patch_and_400(
            "/namespaces/namespaceone", {"created_at": "2022-01-01"}
        )
        self.assert_patch_and_400(
            "/namespaces/namespaceone", {"nosuchkey": "2022-01-01"}
        )

        # NOTICE: Comma, not colon. This leads to a set being serialized as a list...
        self.assert_patch_and_400("/namespaces/namespaceone", {"not_a", "dict"})
        self.assert_delete("/namespaces/namespaceone")

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

    def test_namespace_get_as_user(self):
        """Test get on namespaces as a normal user."""
        # This creates the user and the group in one go.
        self.client = userclient = self.get_user_client(
            username="tmp", groupname="tmpgroup"
        )
        self.client = self.get_superuser_client()
        self.assert_post("/namespaces/", {"name": "yes"})
        self.assert_post("/namespaces/", {"name": "no"})
        self.assert_post_and_204("/namespaces/yes/groups/tmpgroup", {"has_read": True})
        self.assert_get_elements("/namespaces/", 2)

        self.client = userclient
        self.assert_get_elements("/namespaces/", 1)
        self.assert_get("/namespaces/yes")
        self.assert_get_and_403("/namespaces/no")
        self.assert_get_and_404("/namespaces/doesnotexist")
        self.assert_patch_and_403("/namespaces/yes", {"name": "maybe"})
        self.assert_delete_and_403("/namespaces/yes")

    def test_namespace_patch_as_user(self):
        """Test patch on namespaces as a normal user."""
        # This creates the user and the group in one go.
        self.client = userclient = self.get_user_client(
            username="tmp", groupname="tmpgroup"
        )
        self.client = self.get_superuser_client()
        self.assert_post("/namespaces/", {"name": "yes"})

        self.client = userclient
        self.assert_patch_and_403("/namespaces/yes", {"name": "maybe"})

        self.client = self.get_superuser_client()
        self.assert_post_and_204(
            "/namespaces/yes/groups/tmpgroup", {"has_update": True}
        )

        self.client = userclient
        self.assert_patch("/namespaces/yes", {"name": "maybe"})
        self.assert_get("/namespaces/maybe")
