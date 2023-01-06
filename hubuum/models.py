"""Models for the hubuum project.

The core Host Model should be lean, and depend on other models for raw data.
"""
# from datetime import datetime

from django.db import models


class Host(models.Model):
    """Host model, a portal into hosts of any kind."""

    name = models.CharField(max_length=255)
    fqdn = models.CharField(max_length=255, blank=True, null=True)
    type = models.ForeignKey(
        "HostType",
        on_delete=models.DO_NOTHING,
        related_name="hosts",
        blank=True,
        null=True,
    )
    serial = models.CharField(max_length=255, blank=True, null=True)
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

    # Here's a doozy. If you delete the auth.group, we should probably assign another owner
    # to every object they had. See https://github.com/terjekv/hubuum/issues/3
    owner = models.ForeignKey(
        "auth.Group", related_name="hosts", on_delete=models.DO_NOTHING
    )
    #    fleet_id = models.IntegerField(blank=True, null=True)

    def __str__(self):
        """Stringify the object, used to represent the object towards users."""
        return self.name

    class Meta:
        """Set permissions and other metadata."""

        permissions = (
            ("hubuum.add_host", "User can add hosts"),
            ("hubuum.change_host", "User can patch hosts"),
            ("hubuum.view_host", "User can read the host"),
            ("hubuum.delete_host", "User can delete the host"),
        )


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


class HostType(models.Model):
    """The type of hosts supported.

    These are a touple of a short name and a description, ie:

    name: mac_laptop
    description: An Apple Laptop running MacOS

    or

    name: std_office_computer
    description: A standard office computer running RHEL
    """

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        """Stringify the object, used to represent the object towards users."""
        return self.name


class Jack(models.Model):
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


class Person(models.Model):
    """A person.

    Persons have rooms. Computers may have people. It's all very cozy.
    """

    username = models.CharField(max_length=255)
    room = models.ForeignKey(
        "Room", models.CASCADE, db_column="room", blank=True, null=True
    )
    section = models.IntegerField(blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)
    email = (models.EmailField(),)
    office_phone = models.CharField(max_length=255, blank=True, null=True)
    mobile_phone = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        """Stringify the object, used to represent the object towards users."""
        return self.username


class PurchaseDocuments(models.Model):
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


class PurchaseOrder(models.Model):
    """Accounting, the order.

    When something is bought there is typically some identifier for the purchase.
    This may help you when it comes to service and maintenance.
    Or disputes about money.
    """

    vendor = models.ForeignKey(
        "Vendor", models.CASCADE, db_column="vendor", blank=True, null=True
    )
    order_date = models.DateTimeField(blank=True, null=True)
    po_number = models.ForeignKey(
        PurchaseDocuments, models.CASCADE, db_column="po_number", blank=True, null=True
    )

    def __str__(self):
        """Stringify the object, used to represent the object towards users."""
        return self.po_number


class Room(models.Model):
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


class Vendor(models.Model):
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
        return self.vendor
