"""Versioned (v1) views for the hubuum models."""
# from ipaddress import ip_address

from django.contrib.auth.models import Group
from django.http import Http404
from rest_framework import generics

from hubuum.filters import HubuumObjectPermissionsFilter
from hubuum.models import (
    Host,
    HostType,
    Jack,
    Namespace,
    Permission,
    Person,
    PurchaseDocuments,
    PurchaseOrder,
    Room,
    User,
    Vendor,
)
from hubuum.permissions import IsSuperOrAdminOrReadOnly, NameSpaceOrReadOnly

from .serializers import (
    GroupSerializer,
    HostSerializer,
    HostTypeSerializer,
    JackSerializer,
    NamespaceSerializer,
    PermissionSerializer,
    PersonSerializer,
    PurchaseDocumentsSerializer,
    PurchaseOrderSerializer,
    RoomSerializer,
    UserSerializer,
    VendorSerializer,
)


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
        value = self.kwargs["val"]
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


class HubuumList(generics.ListCreateAPIView):
    """Get: List objects. Post: Add object."""

    permission_classes = (IsSuperOrAdminOrReadOnly,)
    filter_backends = [HubuumObjectPermissionsFilter]


# NOTE: Order for the inheritance here is vital.
class HubuumDetail(MultipleFieldLookupORMixin, generics.RetrieveUpdateDestroyAPIView):
    """Get, Patch, or Destroy an object."""

    permission_classes = (IsSuperOrAdminOrReadOnly,)


class UserList(HubuumList):
    """Get: List users. Post: Add user."""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(HubuumDetail):
    """Get, Patch, or Destroy a user."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_fields = ("id", "username", "email")


class GroupList(HubuumList):
    """Get: List groups. Post: Add group."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class GroupDetail(HubuumDetail):
    """Get, Patch, or Destroy a group."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    lookup_fields = ("id", "name")


class PermissionList(HubuumList):
    """Get: List permissions. Post: Add permission."""

    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer


class PermissionDetail(HubuumDetail):
    """Get, Patch, or Destroy a permission."""

    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer


class HostList(HubuumList):
    """Get: List hosts. Post: Add host."""

    queryset = Host.objects.all().order_by("id")
    serializer_class = HostSerializer


class HostDetail(HubuumDetail):
    """Get, Patch, or Destroy a host."""

    queryset = Host.objects.all()
    serializer_class = HostSerializer
    lookup_fields = ("id", "name", "fqdn")


class NamespaceList(HubuumList):
    """Get: List Namespaces. Post: Add Namespace."""

    queryset = Namespace.objects.all()
    serializer_class = NamespaceSerializer
    permission_classes = (NameSpaceOrReadOnly,)


class NamespaceDetail(HubuumDetail):
    """Get, Patch, or Destroy a namespace."""

    queryset = Namespace.objects.all()
    serializer_class = NamespaceSerializer
    lookup_fields = ("id", "name")
    permission_classes = (NameSpaceOrReadOnly,)


class HostTypeList(HubuumList):
    """Get: List hosttypes. Post: Add hosttype."""

    queryset = HostType.objects.all().order_by("name")
    serializer_class = HostTypeSerializer


class HostTypeDetail(HubuumDetail):
    """Get, Patch, or Destroy a hosttype."""

    queryset = HostType.objects.all()
    serializer_class = HostTypeSerializer


class RoomList(HubuumList):
    """Get: List rooms. Post: Add room."""

    queryset = Room.objects.all().order_by("id")
    serializer_class = RoomSerializer


class RoomDetail(HubuumDetail):
    """Get, Patch, or Destroy a room."""

    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class JackList(HubuumList):
    """Get: List jacks. Post: Add jack."""

    queryset = Jack.objects.all().order_by("name")
    serializer_class = JackSerializer


class JackDetail(HubuumDetail):
    """Get, Patch, or Destroy a jack."""

    queryset = Jack.objects.all()
    serializer_class = JackSerializer


class PersonList(HubuumList):
    """Get: List persons. Post: Add person."""

    queryset = Person.objects.all().order_by("id")
    serializer_class = PersonSerializer


class PersonDetail(HubuumDetail):
    """Get, Patch, or Destroy a person."""

    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class VendorList(HubuumList):
    """Get: List vendors. Post: Add vendor."""

    queryset = Vendor.objects.all().order_by("vendor_name")
    serializer_class = VendorSerializer


class VendorDetail(HubuumDetail):
    """Get, Patch, or Destroy a vendor."""

    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


class PurchaseOrderList(HubuumList):
    """Get: List purchaseorders. Post: Add purchaseorder."""

    queryset = PurchaseOrder.objects.all().order_by("id")
    serializer_class = PurchaseOrderSerializer


class PurchaseOrderDetail(HubuumDetail):
    """Get, Patch, or Destroy a purchaseorder."""

    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer


class PurchaseDocumentList(HubuumList):
    """Get: List purchasedocuments. Post: Add purchasedocument."""

    queryset = PurchaseDocuments.objects.all().order_by("id")
    serializer_class = PurchaseDocumentsSerializer


class PurchaseDocumentDetail(HubuumDetail):
    """Get, Patch, or Destroy a purchasedocument."""

    queryset = PurchaseDocuments.objects.all()
    serializer_class = PurchaseDocumentsSerializer
