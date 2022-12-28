from rest_framework import serializers

from hubuum.models import *

# serializers.HyperlinkedModelSerializer
class HostSerializer(serializers.ModelSerializer):
#    externals = serializers.SerializerMethodField()

    class Meta:
        model = Host
        fields = '__all__'

#    def get_externals(self, obj):
#        associated_externals = DetectedHostData.get_externals_for_host(obj.id)

class ExternalSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalSource
        fields = '__all__'

class DetectedHostDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetectedHostData
        fields = '__all__'

class HostTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostType
        fields = '__all__'

class JackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jack
        fields = '__all__'

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class PurchaseDocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseDocuments
        fields = '__all__'

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'
