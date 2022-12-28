from url_filter.integrations.drf import DjangoFilterBackend
from rest_framework import generics

# Default
# from rest_framework.permissions import IsAuthenticated

#class UserViewSet(ModelViewSet):
#    queryset = User.objects.all()
#    serializer_class = UserSerializer
#    filter_backends = [DjangoFilterBackend]
#    filter_fields = ['username', 'email']

# from url_filter.filtersets import ModelFilterSet
# from rest_framework import viewsets

from .serializers import *
from hubuum.models import *

class HostList(generics.ListCreateAPIView):
    queryset = Host.objects.all().order_by('id')
    serializer_class = HostSerializer
    filter_backends = [DjangoFilterBackend]

class Host(generics.RetrieveUpdateDestroyAPIView):
    queryset = Host.objects.all()
    serializer_class = HostSerializer

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
    queryset = HostType.objects.all().order_by('name')
    serializer_class = HostTypeSerializer
    filter_backends = [DjangoFilterBackend]
    lookup_field = 'name'

class HostType(generics.RetrieveUpdateDestroyAPIView):
    queryset = HostType.objects.all()
    serializer_class = HostTypeSerializer

class RoomList(generics.ListCreateAPIView):
    queryset = Room.objects.all().order_by('id')
    serializer_class = RoomSerializer
    filter_backends = [DjangoFilterBackend]

class Room(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class JackList(generics.ListCreateAPIView):
    queryset = Jack.objects.all().order_by('name')
    serializer_class = JackSerializer
    filter_backends = [DjangoFilterBackend]
    lookup_field = 'name'

class Jack(generics.RetrieveUpdateDestroyAPIView):
    queryset = Jack.objects.all()
    serializer_class = JackSerializer

class PersonList(generics.ListCreateAPIView):
    queryset = Person.objects.all().order_by('id')
    serializer_class = PersonSerializer
    filter_backends = [DjangoFilterBackend]

class Person(generics.RetrieveUpdateDestroyAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

class VendorList(generics.ListCreateAPIView):
    queryset = Vendor.objects.all().order_by('vendor_name')
    serializer_class = VendorSerializer
    filter_backends = [DjangoFilterBackend]
    lookup_field = 'vendor_name'

class Vendor(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class PurchaseOrderList(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all().order_by('id')
    serializer_class = PurchaseOrderSerializer
    filter_backends = [DjangoFilterBackend]

class PurchaseOrder(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class PurchaseDocumentList(generics.ListCreateAPIView):
    queryset = PurchaseDocuments.objects.all().order_by('id')
    serializer_class = PurchaseDocumentsSerializer
    filter_backends = [DjangoFilterBackend]

class PurchaseDocument(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseDocuments.objects.all()
    serializer_class = PurchaseDocumentsSerializer

