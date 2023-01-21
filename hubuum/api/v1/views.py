"""Versioned (v1) views for the hubuum models."""
# from ipaddress import ip_address

from django.contrib.auth.models import Group
from django.http import Http404, HttpResponseBadRequest

# from django.shortcuts import get
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated

# from rest_framework.response import Response
from url_filter.integrations.drf import DjangoFilterBackend

# from guardian.shortcuts import get_objects_for_user

from hubuum.filters import DjangoObjectPermissionsFilter
from hubuum.permissions import CustomObjectPermissions

# Default
# from rest_framework.permissions import IsAuthenticated

# class UserViewSet(ModelViewSet):
#    queryset = User.objects.all()
#    serializer_class = UserSerializer
#    filter_backends = [DjangoFilterBackend]
#    filter_fields = ['username', 'email']

# from url_filter.filtersets import ModelFilterSet
# from rest_framework import viewsets

from hubuum.models import (
    User,
    Host,
    Namespace,
    #    ExternalSource,
    #    DetectedHostData,
    HostType,
    Room,
    Jack,
    Vendor,
    Person,
    PurchaseOrder,
    PurchaseDocuments,
)

from .serializers import (
    HostSerializer,
    NamespaceSerializer,
    #    ExternalSourceSerializer,
    #    DetectedHostDataSerializer,
    HostTypeSerializer,
    RoomSerializer,
    JackSerializer,
    VendorSerializer,
    PersonSerializer,
    PurchaseOrderSerializer,
    PurchaseDocumentsSerializer,
    UserSerializer,
    GroupSerializer,
)


def _write_actions():
    return ["POST", "DELETE", "PATCH"]


def _write_actions_require_admin(self):
    return _actions_requires_admin(self, _write_actions())


def _actions_requires_admin(self, actions):
    if self.request.method in actions:
        permission_classes = [IsAdminUser]
    else:
        permission_classes = [IsAuthenticated]
    return [permission() for permission in permission_classes]


class WriteActionsRequireAdminMixin(object):
    """A mixin that ensures that only admins can perform actions.

    Everyone authenticated is given view/read access.
    """

    def get_permissions(self):
        """Restrict destructive actions to admin."""
        return _write_actions_require_admin(self)


class MultipleFieldLookupORMixin(object):
    """A mixin to allow us to look up objects beyond just the primary key.

    Set lookup_fields in the class to select what fields, in the given order,
    that are used for the lookup. The value is the parameter passed at all times.

    Example: We are passed "foo" as the value to look up (using the key 'lookup_value'),
    and the class has the following set:

    lookup_fields = ("id", "username", "email")

    Applying this mixin will make the class attempt to:
      1. Try to find object where id=foo (the default behaviour)
      2. If no match was found, try to find an object where username=foo
      3. If still no match, try to find an object where email=foo

    If no matches are found, return 404.
    """

    def get_object(self):
        """Perform the actual lookup based on the lookup_fields."""
        queryset = self.get_queryset()
        object = None
        value = self.kwargs["lookup_value"]
        for field in self.lookup_fields:
            try:
                # https://stackoverflow.com/questions/9122169/calling-filter-with-a-variable-for-field-name
                # No, just no.
                object = queryset.get(**{field: value})
                if object:
                    break

            # If we didn't get a hit, or an error, keep trying.
            # If we don't get a hit at all, we'll raise 404.
            except Exception:  # nosec
                pass

        if object is None:
            raise Http404()

        return object


class UserList(WriteActionsRequireAdminMixin, generics.ListCreateAPIView):
    """Get: List users. Post: Add user."""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(
    WriteActionsRequireAdminMixin,
    MultipleFieldLookupORMixin,
    generics.RetrieveUpdateDestroyAPIView,
):
    """Get, Patch, or Destroy a user."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_fields = ("id", "username", "email")


class GroupList(WriteActionsRequireAdminMixin, generics.ListCreateAPIView):
    """Get: List groups. Post: Add group."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


# 5
# TODO: Should we restrict patch and destroy of users and groups to admins? Probably.
class GroupDetail(
    WriteActionsRequireAdminMixin,
    MultipleFieldLookupORMixin,
    generics.RetrieveUpdateDestroyAPIView,
):
    """Get, Patch, or Destroy a group."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    lookup_fields = ("id", "name")


class HostList(generics.ListCreateAPIView):
    """Get: List hosts. Post: Add host."""

    queryset = Host.objects.all().order_by("id")
    serializer_class = HostSerializer
    #    filter_backends = [DjangoFilterBackend]
    permission_classes = (CustomObjectPermissions,)
    filter_backends = (DjangoObjectPermissionsFilter,)


class Host(MultipleFieldLookupORMixin, generics.RetrieveUpdateDestroyAPIView):
    """Get, Patch, or Destroy a host."""

    queryset = Host.objects.all()
    serializer_class = HostSerializer
    lookup_fields = ("id", "name", "fqdn")


class NamespaceList(generics.ListCreateAPIView):
    """Get: List Namespaces. Post: Add Namespace."""

    queryset = Namespace.objects.all()
    serializer_class = NamespaceSerializer
    #    filter_backends = [DjangoFilterBackend]
    permission_classes = (CustomObjectPermissions,)
    filter_backends = (DjangoObjectPermissionsFilter,)


class Namespace(MultipleFieldLookupORMixin, generics.RetrieveUpdateDestroyAPIView):
    """Get, Patch, or Destroy a host."""

    queryset = Namespace.objects.all()
    serializer_class = NamespaceSerializer
    lookup_fields = ("id", "name")


# class ExternalSource(generics.RetrieveUpdateDestroyAPIView):
#     queryset = ExternalSource.objects.all()
#     serializer_class = ExternalSourceSerializer


# class ExternalSourceList(generics.ListCreateAPIView):
#     #    queryset = ExternalSource.objects.all()
#     serializer_class = ExternalSourceSerializer
#     filter_backends = [DjangoFilterBackend]


# class DetectedHost(generics.RetrieveUpdateDestroyAPIView):
#     queryset = DetectedHostData.objects.all()
#     serializer_class = DetectedHostDataSerializer


class HostTypeList(generics.ListCreateAPIView):
    """Get: List hosttypes. Post: Add hosttype."""

    queryset = HostType.objects.all().order_by("name")
    serializer_class = HostTypeSerializer
    filter_backends = [DjangoFilterBackend]
    lookup_field = "name"


class HostType(generics.RetrieveUpdateDestroyAPIView):
    """Get, Patch, or Destroy a hosttype."""

    queryset = HostType.objects.all()
    serializer_class = HostTypeSerializer


class RoomList(generics.ListCreateAPIView):
    """Get: List rooms. Post: Add room."""

    queryset = Room.objects.all().order_by("id")
    serializer_class = RoomSerializer
    filter_backends = [DjangoFilterBackend]


class Room(generics.RetrieveUpdateDestroyAPIView):
    """Get, Patch, or Destroy a room."""

    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class JackList(generics.ListCreateAPIView):
    """Get: List jacks. Post: Add jack."""

    queryset = Jack.objects.all().order_by("name")
    serializer_class = JackSerializer
    filter_backends = [DjangoFilterBackend]
    lookup_field = "name"


class Jack(generics.RetrieveUpdateDestroyAPIView):
    """Get, Patch, or Destroy a jack."""

    queryset = Jack.objects.all()
    serializer_class = JackSerializer


class PersonList(generics.ListCreateAPIView):
    """Get: List persons. Post: Add person."""

    queryset = Person.objects.all().order_by("id")
    serializer_class = PersonSerializer
    filter_backends = [DjangoFilterBackend]


class Person(generics.RetrieveUpdateDestroyAPIView):
    """Get, Patch, or Destroy a person."""

    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class VendorList(generics.ListCreateAPIView):
    """Get: List vendors. Post: Add vendor."""

    queryset = Vendor.objects.all().order_by("vendor_name")
    serializer_class = VendorSerializer
    filter_backends = [DjangoFilterBackend]
    lookup_field = "vendor_name"


class Vendor(generics.RetrieveUpdateDestroyAPIView):
    """Get, Patch, or Destroy a vendor."""

    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


class PurchaseOrderList(generics.ListCreateAPIView):
    """Get: List purchaseorders. Post: Add purchaseorder."""

    queryset = PurchaseOrder.objects.all().order_by("id")
    serializer_class = PurchaseOrderSerializer
    filter_backends = [DjangoFilterBackend]


class PurchaseOrder(generics.RetrieveUpdateDestroyAPIView):
    """Get, Patch, or Destroy a purchaseorder."""

    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer


class PurchaseDocumentList(generics.ListCreateAPIView):
    """Get: List purchasedocuments. Post: Add purchasedocument."""

    queryset = PurchaseDocuments.objects.all().order_by("id")
    serializer_class = PurchaseDocumentsSerializer
    filter_backends = [DjangoFilterBackend]


class PurchaseDocument(generics.RetrieveUpdateDestroyAPIView):
    """Get, Patch, or Destroy a purchasedocument."""

    queryset = PurchaseDocuments.objects.all()
    serializer_class = PurchaseDocumentsSerializer
