"""Versioned (v1) serializers of the hubuum models."""
from django.contrib.auth.models import User, Group
from rest_framework import serializers

from hubuum.models import (
    Host,
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


class UserSerializer(serializers.ModelSerializer):
    """Serialize a User object."""

    #    def create(self, validated_data):
    #        user = User.objects.create_user(**validated_data)
    #        return user

    class Meta:
        """How to serialize the object."""

        model = User
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer):
    """Serialize a Group object."""

    #    def create(self, validated_data):
    #        group = Group.objects.create_user(**validated_data)
    #        return group
    class Meta:
        """How to serialize the object."""

        model = Group
        fields = "__all__"


class HostSerializer(serializers.ModelSerializer):
    """Serialize a Host object."""

    # serializers.HyperlinkedModelSerializer
    #    externals = serializers.SerializerMethodField()
    #    _mod_dns = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())

    class Meta:
        """How to serialize the object."""

        model = Host
        fields = "__all__"
        # fields = ['id', 'name', '_mod_dns']


#    def get_externals(self, obj):
#        associated_externals = DetectedHostData.get_externals_for_host(obj.id)


# class ExternalSourceSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = ExternalSource
#        fields = "__all__"


# class DetectedHostDataSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = DetectedHostData
#        fields = "__all__"


class HostTypeSerializer(serializers.ModelSerializer):
    """Serialize a HostType object."""

    class Meta:
        """How to serialize the object."""

        model = HostType
        fields = "__all__"


class JackSerializer(serializers.ModelSerializer):
    """Serialize a Jack object."""

    class Meta:
        """How to serialize the object."""

        model = Jack
        fields = "__all__"


class PersonSerializer(serializers.ModelSerializer):
    """Serialize a Person object."""

    class Meta:
        """How to serialize the object."""

        model = Person
        fields = "__all__"


class RoomSerializer(serializers.ModelSerializer):
    """Serialize a Room object."""

    class Meta:
        """How to serialize the object."""

        model = Room
        fields = "__all__"


class PurchaseDocumentsSerializer(serializers.ModelSerializer):
    """Serialize a PurchaseDocument object."""

    class Meta:
        """How to serialize the object."""

        model = PurchaseDocuments
        fields = "__all__"


class PurchaseOrderSerializer(serializers.ModelSerializer):
    """Serialize a PurchaseOrder object."""

    class Meta:
        """How to serialize the object."""

        model = PurchaseOrder
        fields = "__all__"


class VendorSerializer(serializers.ModelSerializer):
    """Serialize a Vendor object."""

    class Meta:
        """How to serialize the object."""

        model = Vendor
        fields = "__all__"
