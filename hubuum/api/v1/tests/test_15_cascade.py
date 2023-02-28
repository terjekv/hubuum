"""Test cascading effects on models."""
from .base import HubuumAPITestCase


class APICascade(HubuumAPITestCase):
    """Test cascading effects on models."""

    def test_cascading_namespaces(self):
        """Test what happens when a namespace goes away."""
        self.client = self.get_superuser_client()
        self.assert_post("/namespaces/", {"name": "yes"})
        nsblob = self.assert_get("/namespaces/yes")
        self.assert_post("/hosts/", {"name": "host1", "namespace": nsblob.data["id"]})
        self.assert_post("/hosts/", {"name": "host2", "namespace": nsblob.data["id"]})
        self.assert_get_elements("/hosts/", 2)
        self.assert_get("/hosts/host1")
        self.assert_delete("/namespaces/yes")
        self.assert_get_elements("/hosts/", 0)

    def test_cascading_permissions(self):
        """Test what happens when a namespace goes away."""
        self.assert_post("/namespaces/", {"name": "yes"})
        self.client = self.get_user_client(username="tmp", groupname="tmpgroup")
        self.grant("tmpgroup", "yes", ["has_read"])
        self.assert_get_elements("/permissions/", 1)
        self.client = self.get_superuser_client()
        self.assert_delete("/groups/tmpgroup")
        self.assert_get_elements("/permissions/", 0)

        self.client = self.get_user_client(username="tmp", groupname="tmpgroup")
        self.assert_get_elements("/permissions/", 0)
        self.grant("tmpgroup", "yes", ["has_read"])
        self.assert_get_elements("/permissions/", 1)
        self.client = self.get_superuser_client()
        self.assert_delete("/namespaces/yes")
        self.assert_get_elements("/permissions/", 0)

        self.assert_post("/namespaces/", {"name": "yes"})
        self.client = self.get_user_client(username="tmp", groupname="tmpgroup")
        self.assert_get_elements("/permissions/", 0)
        self.grant("tmpgroup", "yes", ["has_read"])
        self.assert_get_elements("/permissions/", 1)
        perms = self.assert_get("/permissions/")
        pid = perms.data[0]["id"]
        self.client = self.get_superuser_client()
        self.assert_delete(f"/permissions/{pid}")
        self.assert_get_elements("/permissions/", 0)
        self.assert_get_elements("/namespaces/", 1)
        self.assert_get_elements("/groups/", 1)

    def test_cascading_groups(self):
        """Test cascading groups."""
        self.client = self.get_user_client(username="tmp", groupname="tmpgroup")
        self.client = self.get_superuser_client()
        self.assert_post("/namespaces/", {"name": "yes"})
        self.grant("tmpgroup", "yes", ["has_read"])
        self.assert_get_elements("/permissions/", 1)
        self.assert_get_elements("/namespaces/", 1)
        self.assert_get_elements("/groups/", 1)

        self.assert_delete("/groups/tmpgroup")
        self.assert_get_elements("/permissions/", 0)
        self.assert_get_elements("/namespaces/", 1)
        self.assert_get_elements("/groups/", 0)
