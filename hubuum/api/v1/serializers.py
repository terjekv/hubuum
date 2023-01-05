from django.contrib.auth.models import User, Group
from rest_framework import serializers

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


class UserSerializer(serializers.ModelSerializer):
    #    def create(self, validated_data):
    #        user = User.objects.create_user(**validated_data)
    #        return user

    class Meta:
        model = User
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer):
    #    def create(self, validated_data):
    #        group = Group.objects.create_user(**validated_data)
    #        return group
    class Meta:
        model = Group
        fields = "__all__"


class HostSerializer(serializers.ModelSerializer):
    # serializers.HyperlinkedModelSerializer
    #    externals = serializers.SerializerMethodField()
    #    _mod_dns = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())

    class Meta:
        model = Host
        fields = "__all__"
        # fields = ['id', 'name', '_mod_dns']


#    def get_externals(self, obj):
#        associated_externals = DetectedHostData.get_externals_for_host(obj.id)


class ExternalSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalSource
        fields = "__all__"


class DetectedHostDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetectedHostData
        fields = "__all__"


class HostTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostType
        fields = "__all__"


class JackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jack
        fields = "__all__"


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = "__all__"


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"


class PurchaseDocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseDocuments
        fields = "__all__"


class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = "__all__"


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = "__all__"
