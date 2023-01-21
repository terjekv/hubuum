"""Provide a base class for testing model behaviour."""

from django.test import TestCase
from django.contrib.auth.models import Group

from django.contrib.auth import get_user_model

from hubuum.exceptions import MissingParam

from hubuum.models import (
    Namespace,
    Room,
    Vendor,
    Person,
    PurchaseOrder,
    PurchaseDocuments,
    #    Permissions,
)


class HubuumModelTestCase(TestCase):
    """This class defines the test suite for a generic model."""

    def setUp(self):
        """Set up defaults for the test object."""
        self.username = "test"
        self.password = "test"
        self.groupname = "test"
        self.namespacename = "test"

        self.user, created = get_user_model().objects.get_or_create(
            username=self.username, password=self.password
        )
        self.assertIsNotNone(self.user)

        self.group, created = Group.objects.get_or_create(name=self.groupname)
        self.assertIsNotNone(self.group)

        self.namespace, created = Namespace.objects.get_or_create(
            name=self.namespacename, description="Test namespace."
        )
        self.assertIsNotNone(self.namespace)

    def attribute(self, key):
        """Fetch attributes from the attribute dictionary."""
        return self.attributes[key]

    def _test_can_create_object(self, model=None, **kwargs):
        """Create a generic object of any model."""
        if "namespace" not in kwargs:
            kwargs["namespace"] = self.namespace

        return self._create_object(model=model, **kwargs)

    def _test_has_identical_values(self, object=None, dictionary=None):
        """Compare the dictionary with the same attributes from the self."""
        if not (object and dictionary):
            raise MissingParam

        for key in dictionary.keys():
            self.assertEqual(getattr(object, key), dictionary[key])

    def _create_object(self, model=None, **kwargs):
        """Create an object with overridable default group ownership."""
        if not model:
            raise MissingParam

        object, created = model.objects.get_or_create(**kwargs)
        self.assertIsNotNone(object)
        self.assertIsInstance(object, model)
        return object

    def _test_str(self):
        """Test that stringifying objects works as expected."""
        object = self.object
        if isinstance(object, Person):
            self.assertEqual(str(object), self.attribute("username"))
        elif isinstance(object, PurchaseDocuments):
            self.assertEqual(str(object), self.attribute("document_id"))
        elif isinstance(object, PurchaseOrder):
            self.assertEqual(str(object), self.attribute("po_number"))
        elif isinstance(object, Room):
            floor = self.attribute("floor").rjust(2, "0")
            building = self.attribute("building")
            room_id = self.attribute("room_id")
            string = building + "-" + floor + "-" + room_id
            self.assertEqual(str(object), string)
        elif isinstance(object, Vendor):
            self.assertEqual(str(object), self.attribute("vendor_name"))
        else:
            self.assertEqual(str(object), self.attribute("name"))