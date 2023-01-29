"""Test hosts."""

from .base import HubuumAPITestCase


class APIHostTestCase(HubuumAPITestCase):
    """Test host operations."""

    def test_superuser_host_operations(self):
        """Test host creation from a superuser."""
        self.client = self.superuserclient
        namespace = self.get_namespace("one")
        response = self.assert_post(
            "/hosts/", {"name": "hostone", "namespace": namespace.data["id"]}
        )
        self.assertEqual(response.data["name"], "hostone")
        self.assert_get("/host/hostone")
        self.assert_patch("/host/hostone", {"fqdn": "hostone.example.org"})
        self.assert_delete("/host/hostone")
