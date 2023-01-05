from ipaddress import ip_address

from django.contrib.auth.models import User, Group
from django.http import Http404

# from django.shortcuts import get
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from url_filter.integrations.drf import DjangoFilterBackend
from guardian.shortcuts import get_objects_for_user

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
    Host,
    ExternalSource,
    DetectedHostData,
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
    ExternalSourceSerializer,
    DetectedHostDataSerializer,
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


def _post_requires_admin(self):
    if self.request.method == "POST":
        permission_classes = [IsAdminUser]
    else:
        permission_classes = [IsAuthenticated]
    return [permission() for permission in permission_classes]


class MultipleFieldLookupORMixin(object):
    def get_object(self):
        queryset = self.get_queryset()
        object = None
        value = self.kwargs["lookup_value"]
        for field in self.lookup_fields:
            try:
                # https://stackoverflow.com/questions/9122169/calling-filter-with-a-variable-for-field-name
                # No, just no.
                object = queryset.get(**{field: value})
            except Exception:
                pass

        if object == None:
            raise Http404()

        return object


class UserList(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()

    def get_permissions(self):
        return _post_requires_admin(self)


class UserDetail(MultipleFieldLookupORMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_fields = ("id", "username", "email")


class GroupList(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def get_permissions(self):
        return _post_requires_admin(self)


class GroupDetail(MultipleFieldLookupORMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    lookup_fields = ("id", "name")


class HostList(generics.ListCreateAPIView):
    queryset = Host.objects.all().order_by("id")
    serializer_class = HostSerializer
    #    filter_backends = [DjangoFilterBackend]
    permission_classes = (CustomObjectPermissions,)
    filter_backends = (DjangoObjectPermissionsFilter,)


class Host(MultipleFieldLookupORMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Host.objects.all()
    serializer_class = HostSerializer
    lookup_fields = ("id", "name", "fqdn")


class ExternalSource(generics.RetrieveUpdateDestroyAPIView):
    queryset = ExternalSource.objects.all()
    serializer_class = ExternalSourceSerializer


class ExternalSourceList(generics.ListCreateAPIView):
    #    queryset = ExternalSource.objects.all()
    serializer_class = ExternalSourceSerializer
    filter_backends = [DjangoFilterBackend]


class DetectedHost(generics.RetrieveUpdateDestroyAPIView):
    queryset = DetectedHostData.objects.all()
    serializer_class = DetectedHostDataSerializer


class HostTypeList(generics.ListCreateAPIView):
    queryset = HostType.objects.all().order_by("name")
    serializer_class = HostTypeSerializer
    filter_backends = [DjangoFilterBackend]
    lookup_field = "name"


class HostType(generics.RetrieveUpdateDestroyAPIView):
    queryset = HostType.objects.all()
    serializer_class = HostTypeSerializer


class RoomList(generics.ListCreateAPIView):
    queryset = Room.objects.all().order_by("id")
    serializer_class = RoomSerializer
    filter_backends = [DjangoFilterBackend]


class Room(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class JackList(generics.ListCreateAPIView):
    queryset = Jack.objects.all().order_by("name")
    serializer_class = JackSerializer
    filter_backends = [DjangoFilterBackend]
    lookup_field = "name"


class Jack(generics.RetrieveUpdateDestroyAPIView):
    queryset = Jack.objects.all()
    serializer_class = JackSerializer


class PersonList(generics.ListCreateAPIView):
    queryset = Person.objects.all().order_by("id")
    serializer_class = PersonSerializer
    filter_backends = [DjangoFilterBackend]


class Person(generics.RetrieveUpdateDestroyAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class VendorList(generics.ListCreateAPIView):
    queryset = Vendor.objects.all().order_by("vendor_name")
    serializer_class = VendorSerializer
    filter_backends = [DjangoFilterBackend]
    lookup_field = "vendor_name"


class Vendor(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


class PurchaseOrderList(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all().order_by("id")
    serializer_class = PurchaseOrderSerializer
    filter_backends = [DjangoFilterBackend]


class PurchaseOrder(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer


class PurchaseDocumentList(generics.ListCreateAPIView):
    queryset = PurchaseDocuments.objects.all().order_by("id")
    serializer_class = PurchaseDocumentsSerializer
    filter_backends = [DjangoFilterBackend]


class PurchaseDocument(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseDocuments.objects.all()
    serializer_class = PurchaseDocumentsSerializer
