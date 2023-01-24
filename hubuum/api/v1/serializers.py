"""Versioned (v1) serializers of the hubuum models."""
from rest_framework.fields import empty
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import Group
from rest_framework import serializers

# from hubuum.models_auth import User

from hubuum.models import (
    User,
    Host,
    Namespace,
    HostType,
    Room,
    Jack,
    Vendor,
    Person,
    PurchaseOrder,
    PurchaseDocuments,
    Permission,
)


class ErrorOnBadFieldMixin:
    """Raise validation errors on bad input.

    Django Rest Framework returns 200 OK for patches against both
    read-only fields and non-existent fields... Ie, a quiet failure.
    This mixin changes that behaviour to raise a Validation error which
    again causes the response "400 Bad Request".
    See https://github.com/encode/django-rest-framework/issues/6508
    """

    def run_validation(self, data=empty):
        """Run the validation of the input."""
        provided_keys = data.keys()
        for fieldname, field in self.fields.items():
            if field.read_only and fieldname in provided_keys:
                raise ValidationError(
                    code="write_on_read_only_field",
                    detail={
                        fieldname: (
                            "You're trying to write to the field "
                            "'{}' which is a read-only field.".format(fieldname)
                        )
                    },
                )

        extra_keys = set(provided_keys) - set(self.fields.keys())
        if extra_keys:
            raise ValidationError(
                code="write_on_non_existent_field",
                detail={
                    fieldname: (
                        "You're trying to write to the field "
                        "'{}' which does not exist.".format(fieldname)
                    )
                },
            )

        return super().run_validation(data)


class HubuumSerializer(ErrorOnBadFieldMixin, serializers.ModelSerializer):
    """General Hubuum Serializer."""


class UserSerializer(HubuumSerializer):
    """Serialize a User object."""

    class Meta:
        """How to serialize the object."""

        model = User
        fields = "__all__"


class GroupSerializer(HubuumSerializer):
    """Serialize a Group object."""

    class Meta:
        """How to serialize the object."""

        model = Group
        fields = "__all__"


class HostSerializer(HubuumSerializer):
    """Serialize a Host object."""

    # serializers.HyperlinkedModelSerializer
    #    externals = serializers.SerializerMethodField()
    #    _mod_dns = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())

    class Meta:
        """How to serialize the object."""

        model = Host
        fields = "__all__"
        # fields = ['id', 'name', '_mod_dns']


class NamespaceSerializer(HubuumSerializer):
    """Serialize a Namespace object."""

    class Meta:
        """How to serialize the object."""

        model = Namespace
        fields = "__all__"


class PermissionSerializer(HubuumSerializer):
    """Serialize a Permission object."""

    class Meta:
        """How to serialize the object."""

        model = Permission
        fields = "__all__"


class HostTypeSerializer(HubuumSerializer):
    """Serialize a HostType object."""

    class Meta:
        """How to serialize the object."""

        model = HostType
        fields = "__all__"


class JackSerializer(HubuumSerializer):
    """Serialize a Jack object."""

    class Meta:
        """How to serialize the object."""

        model = Jack
        fields = "__all__"


class PersonSerializer(HubuumSerializer):
    """Serialize a Person object."""

    class Meta:
        """How to serialize the object."""

        model = Person
        fields = "__all__"


class RoomSerializer(HubuumSerializer):
    """Serialize a Room object."""

    class Meta:
        """How to serialize the object."""

        model = Room
        fields = "__all__"


class PurchaseDocumentsSerializer(HubuumSerializer):
    """Serialize a PurchaseDocument object."""

    class Meta:
        """How to serialize the object."""

        model = PurchaseDocuments
        fields = "__all__"


class PurchaseOrderSerializer(HubuumSerializer):
    """Serialize a PurchaseOrder object."""

    class Meta:
        """How to serialize the object."""

        model = PurchaseOrder
        fields = "__all__"


class VendorSerializer(HubuumSerializer):
    """Serialize a Vendor object."""

    class Meta:
        """How to serialize the object."""

        model = Vendor
        fields = "__all__"
