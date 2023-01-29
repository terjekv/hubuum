"""Models for the hubuum project."""
# from datetime import datetime
import re

from django.apps import apps
from django.contrib.auth.models import AbstractUser
from django.db import models

from hubuum.exceptions import MissingParam
from hubuum.permissions import operation_exists


def model_exists(model):
    """Check if a given model exists by name."""
    return apps.get_model("hubuum", model)


def model_is_open(model):
    """Check if the model is an open model."""
    return model in models_that_are_open()


def models_that_are_open():
    """Return a list of models open to all authenticated users."""
    return ("user", "group")


class User(AbstractUser):
    """Extension to the default User class."""

    permissions_pattern = re.compile(r"^hubuum.(\w+)_(\w+)$")

    _group_list = None

    def is_admin(self):
        """Check if the user is any type of admin (staff/superadmin) (or in a similar group?)."""
        return self.is_staff or self.is_superuser

    @property
    def group_list(self):
        """List the names of all the groups the user is a member of."""
        if self._group_list is None:
            self._group_list = list(self.groups.values_list("name", flat=True))
        return self._group_list

    def can_modify_namespaces(self, namespace):
        """Check if the user has namespace permissions for the given namespace.

        If the namespace isn't scoped (contains no dots), return False.
        Only admin users can create root namespaces.
        """
        scope = namespace.split(".")

        if len(scope) == 0:
            return False

        try:
            parent = Namespace.objects.get(name=scope[-1])
        except Namespace.DoesNotExist:
            return False

        return Permission.objects.filter(
            namespace=parent.id, has_namespace=True, group__in=self.groups.all()
        ).exists()

    def has_perm(self, perm: str, obj: object = None) -> bool:
        """
        Permissions check for an object.

        perm: see permissions.py
        obj: Hubuum Object
        """
        #        print("Self: <" + str(self) + ">")
        #        print("Perm: <" + str(perm) + ">")
        #        print("Obj: <" + str(obj) + "> (" + str(obj.__class__) + ")")

        field = None

        try:
            operation, model = re.match(User.permissions_pattern, perm).groups()
        except AttributeError as exc:
            raise MissingParam(
                f"Unknown permission '{perm}' passed to has_perm"
            ) from exc

        if not (operation and model):
            raise MissingParam(f"Unknown expression '{perm}' passed to has_perm")

        if operation_exists(operation) and model_exists(model):
            field = "has_" + operation
        else:
            raise MissingParam(
                f"Unknown operation or model '{operation} / {model}' passed to has_perm"
            )

        if obj:
            return Permission.objects.filter(
                namespace=obj.namespace, **{field: True}, group__in=self.groups.all()
            ).exists()

        return False


class HubuumModel(models.Model):
    """Base model for Hubuum Objects."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta data for the class."""

        abstract = True


class NamespacedHubuumModel(HubuumModel):
    """Base model for a namespaced Hubuum Objects."""

    namespace = models.ForeignKey(
        "Namespace",
        on_delete=models.DO_NOTHING,
        blank=False,
        null=False,
    )

    class Meta:
        """Meta data for the class."""

        abstract = True


class Namespace(HubuumModel):
    """The namespace ('domain') of an object."""

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)


class Permission(HubuumModel):
    """
    Permissions in Hubuum.

    - Permissions are set by group.
    - Objects belong to a namespace.
    - Every namespace has zero or more groups with permissions for the namespace.

    The permission `has_namespace` allows for the group to create new namespaces scoped
    under the current one.

    """

    namespace = models.ForeignKey(
        "Namespace", related_name="p_namespace", on_delete=models.CASCADE
    )
    group = models.ForeignKey(
        "auth.Group", related_name="p_group", on_delete=models.CASCADE
    )

    has_create = models.BooleanField(null=False, default=False)
    has_read = models.BooleanField(null=False, default=False)
    has_update = models.BooleanField(null=False, default=False)
    has_delete = models.BooleanField(null=False, default=False)
    has_namespace = models.BooleanField(null=False, default=False)

    class Meta:
        """Metadata permissions."""

        unique_together = (
            "namespace",
            "group",
        )


class Host(NamespacedHubuumModel):
    """Host model, a portal into hosts of any kind."""

    name = models.CharField(max_length=255)
    fqdn = models.CharField(max_length=255, blank=True)
    type = models.ForeignKey(
        "HostType",
        on_delete=models.DO_NOTHING,
        related_name="hosts",
        blank=True,
        null=True,
    )
    serial = models.CharField(max_length=255, blank=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(
        "Room", on_delete=models.DO_NOTHING, related_name="hosts", blank=True, null=True
    )
    jack = models.ForeignKey(
        "Jack", on_delete=models.DO_NOTHING, related_name="hosts", blank=True, null=True
    )
    purchase_order = models.ForeignKey(
        "PurchaseOrder",
        on_delete=models.DO_NOTHING,
        related_name="hosts",
        blank=True,
        null=True,
    )

    person = models.ForeignKey(
        "Person",
        on_delete=models.DO_NOTHING,
        related_name="hosts",
        blank=True,
        null=True,
    )

    namespace = models.ForeignKey(
        "Namespace",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )

    def __str__(self):
        """Stringify the object, used to represent the object towards users."""
        return self.name


# Unique names sounds like a good idea, but "bob's laptop" might happen repeatedly.
# Serial numbers are also only vendor-unique...
#    class Meta:
#        constraints = [
#            models.UniqueConstraint(
#                fields=['name'], name="unique_hostname_constraint",
#            )
#        ]


# class ExternalSource(models.Model):
#     service_name = models.CharField(max_length=255)
#     web_url = models.CharField(max_length=255, blank=True, null=True)
#     api_url = models.CharField(max_length=255, blank=True, null=True)

#     def __str__(self):
#         """Stringify the object, used to represent the object towards users."""
#         return self.service_name


# class DetectedHostData(models.Model):
#     host_id = models.OneToOneField(
#         Host, verbose_name="Host identifier", on_delete=models.CASCADE
#     )
#     source = models.OneToOneField(ExternalSource, on_delete=models.CASCADE)
#     fqdn = models.CharField(max_length=255, blank=True, null=True)
#     serial_number = models.CharField(max_length=50, blank=True, null=True)
#     mac = models.CharField(
#         max_length=20, blank=True, null=True
#     )  # https://github.com/django-macaddress/django-macaddress
#     ipv4_address = models.GenericIPAddressField(blank=True, null=True, protocol="IPv4")
#     ipv6_address = models.GenericIPAddressField(blank=True, null=True, protocol="IPv6")
#     memory = models.IntegerField(blank=True, null=True)
#     cpu = models.CharField(max_length=50, blank=True, null=True)
#     arch = models.CharField(max_length=10, blank=True, null=True)
#     model = models.CharField(max_length=50, blank=True, null=True)
#     vendor = models.CharField(max_length=50, blank=True, null=True)
#     os = models.CharField(max_length=20, blank=True, null=True)
#     os_major_version = models.SmallIntegerField(blank=True, null=True)
#     os_minor_version = models.SmallIntegerField(blank=True, null=True)
#     os_patch_version = models.SmallIntegerField(blank=True, null=True)
#     last_fetched = models.DateTimeField(blank=True, null=True)
#     switch = models.CharField(max_length=255, blank=True, null=True)
#     port = models.CharField(max_length=30, blank=True, null=True)
#     display = models.CharField(max_length=50, blank=True, null=True)
#     primary_user = models.CharField(max_length=50, blank=True, null=True)

#     class Meta:
#         verbose_name_plural = "detected host Data"
#         constraints = [
#             models.UniqueConstraint(
#                 fields=["host_id", "source"], name="host_id_and_source_combination"
#             )
#         ]

#     def __str__(self):
#         """Stringify the object, used to represent the object towards users."""
#         return Host.objects.get(pk=self.id).name + "+" + self.source

#     # Should also support other identifiers?
#     @staticmethod
#     def get_externals_for_host(hostid):
#         try:
#             objects = DetectedHostData.objects.get(hostid=hostid)
#         except DetectedHostData.DoesNotExist:
#             objects = []
#         return DetectedHostData.objects.get(hostid=hostid)


class HostType(NamespacedHubuumModel):
    """The type of hosts supported.

    These are a touple of a short name and a description, ie:

    name: mac_laptop
    description: An Apple Laptop running MacOS

    or

    name: std_office_computer
    description: A standard office computer running RHEL
    """

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        """Stringify the object, used to represent the object towards users."""
        return self.name


class Jack(NamespacedHubuumModel):
    """The wall end of a network jack.

    Like the marking of power outlets, there are standards for such things.
    In Norway, the relevant standard is NS 3457-7.
    https://www.standard.no/fagomrader/bygg-anlegg-og-eiendom/ns-3420-/klassifikasjon-av-byggverk---ns-3457/

    Typically, a jack exists in a room. You an also set a building if your room
    identifier by itself isn't unique.
    """

    name = models.CharField(max_length=255)
    room = models.ForeignKey(
        "Room", models.CASCADE, db_column="room", blank=True, null=True
    )
    building = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        """Stringify the object, used to represent the object towards users."""
        return self.name


class Person(NamespacedHubuumModel):
    """A person.

    Persons have rooms. Computers may have people. It's all very cozy.
    """

    username = models.CharField(max_length=255)
    room = models.ForeignKey(
        "Room", models.CASCADE, db_column="room", blank=True, null=True
    )
    section = models.IntegerField(blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    office_phone = models.CharField(max_length=255, blank=True, null=True)
    mobile_phone = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        """Stringify the object, used to represent the object towards users."""
        return self.username


class PurchaseDocuments(NamespacedHubuumModel):
    """Accounting, the documents of an order.

    The documents that came with a given purchase order.
    """

    document_id = models.CharField(max_length=255)
    purchase_order = models.ForeignKey(
        "PurchaseOrder", models.CASCADE, blank=False, null=False
    )
    document = models.BinaryField(blank=False, null=False)

    class Meta:
        """Set permissions and other metadata."""

        verbose_name_plural = "purchase documents"

    def __str__(self):
        """Stringify the object, used to represent the object towards users."""
        return self.document_id


class PurchaseOrder(NamespacedHubuumModel):
    """Accounting, the order.

    When something is bought there is typically some identifier for the purchase.
    This may help you when it comes to service and maintenance.
    Or disputes about money.
    """

    vendor = models.ForeignKey(
        "Vendor", models.CASCADE, db_column="vendor", blank=True, null=True
    )
    order_date = models.DateTimeField(blank=True, null=True)
    po_number = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        """Stringify the object, used to represent the object towards users."""
        return str(self.po_number)


class Room(NamespacedHubuumModel):
    """A room.

    Possibly with a view. If your room_id contains a floor or building identifier, feel free to
    ignore the those fields. If your organization repeats room identifiers between buildings,
    you have my sympathies. If they repeat the room identifier per floor, well, ouch.
    """

    room_id = models.CharField(max_length=255)
    building = models.CharField(max_length=255, blank=True, null=True)
    floor = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        """Stringify the object, used to represent the object towards users."""
        return self.building + "-" + self.floor.rjust(2, "0") + "-" + self.room_id


class Vendor(NamespacedHubuumModel):
    """A vendor, they sell you things.

    Say thank you. Call your vendor today.
    """

    vendor_name = models.CharField(max_length=255)
    vendor_url = models.URLField()
    vendor_credentials = models.CharField(max_length=255, blank=True, null=True)
    contact_name = models.CharField(max_length=255, blank=True, null=True)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        """Stringify the object, used to represent the object towards users."""
        return self.vendor_name
