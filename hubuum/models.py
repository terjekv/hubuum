# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from django.db import models

class Host(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    type = models.ForeignKey('HostType', models.CASCADE, blank=True, null=True)
    serial = models.CharField(max_length=255, blank=True, null=True)
    registration_date = models.DateTimeField(blank=True, null=True)
    room = models.ForeignKey('Room', models.CASCADE, blank=True, null=True)
    jack = models.ForeignKey('Jack', models.CASCADE, blank=True, null=True)
    purchase_order = models.ForeignKey('PurchaseOrder', models.CASCADE, blank=True, null=True)
#    fleet_id = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

# Unique names sounds like a good idea, but "bob's laptop" might happen repeatedly. 
# Serial numbers are also only vendor-unique...
#    class Meta:
#        constraints = [
#            models.UniqueConstraint(
#                fields=['name'], name="unique_hostname_constraint",
#            )
#        ]

class ExternalSource(models.Model):
    service_name = models.CharField(max_length=255)
    web_url = models.CharField(max_length=255, blank=True, null=True)
    api_url = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.service_name

class DetectedHostData(models.Model):
    host_id = models.OneToOneField(Host, verbose_name="Host identifier", on_delete=models.CASCADE)
    source = models.OneToOneField(ExternalSource, on_delete=models.CASCADE)
    dns = models.CharField(max_length=255, blank=True, null=True)
    serial_number = models.CharField(max_length=50, blank=True, null=True)
    mac = models.CharField(max_length=20, blank=True, null=True)  # https://github.com/django-macaddress/django-macaddress
    ipv4_address = models.GenericIPAddressField(blank=True, null=True, protocol="IPv4")
    ipv6_address = models.GenericIPAddressField(blank=True, null=True, protocol="IPv6")
    memory = models.IntegerField(blank=True, null=True)
    cpu = models.CharField(max_length=50, blank=True, null=True)
    arch = models.CharField(max_length=10, blank=True, null=True)
    model = models.CharField(max_length=50, blank=True, null=True)
    vendor = models.CharField(max_length=50, blank=True, null=True)
    os = models.CharField(max_length=20, blank=True, null=True)
    os_major_version = models.SmallIntegerField(blank=True, null=True)
    os_minor_version = models.SmallIntegerField(blank=True, null=True)
    os_patch_version = models.SmallIntegerField(blank=True, null=True)
    last_fetched = models.DateTimeField(blank=True, null=True)
    switch = models.CharField(max_length=255, blank=True, null=True)
    port = models.CharField(max_length=30, blank=True, null=True)
    display = models.CharField(max_length=50, blank=True, null=True)
    primary_user = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name_plural = "detected host Data"
        constraints = [
            models.UniqueConstraint(
                fields=['host_id', 'source'], name='host_id_and_source_combination'
            )
        ]

    def __str__(self):
        return Host.objects.get(pk = self.id).name + "+" + self.source
    
    # Should also support other identifiers?
    @staticmethod
    def get_externals_for_host(hostid):
        try:
            objects = DetectedHostData.objects.get(hostid=hostid)
        except DetectedHostData.DoesNotExist:
            objects = []
        return DetectedHostData.objects.get(hostid=hostid)

class HostType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Jack(models.Model):
    name = models.CharField(max_length=255)
    room = models.ForeignKey('Room', models.CASCADE, db_column='room', blank=True, null=True)
    building = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class Person(models.Model):
    username = models.CharField(max_length=255)
    room = models.ForeignKey('Room', models.CASCADE, db_column='room', blank=True, null=True)
    section = models.IntegerField(blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(),
    office_phone = models.CharField(max_length=255, blank=True, null=True)
    mobile_phone = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username

class PurchaseDocuments(models.Model):
    document_id = models.CharField(max_length=255)
    purchase_order = models.ForeignKey("PurchaseOrder", models.CASCADE, blank=False, null=False)
    document = models.BinaryField(blank=False, null=False)

    class Meta:
        verbose_name_plural = "purchase documents"

    def __str__(self):
        return self.document_id

class PurchaseOrder(models.Model):
    vendor = models.ForeignKey('Vendor', models.CASCADE, db_column='vendor', blank=True, null=True)
    order_date = models.DateTimeField(blank=True, null=True)
    po_number = models.ForeignKey(PurchaseDocuments, models.CASCADE, db_column='po_number', blank=True, null=True)

    def __str__(self):
        return self.po_number

class Room(models.Model):
    room_id = models.CharField(max_length=255)
    building = models.CharField(max_length=255, blank=True, null=True)
    floor = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.building + "-" + self.floor.rjust(2, "0") + "-" + self.room_id

class Vendor(models.Model):
    vendor_name = models.CharField(max_length=255)
    vendor_url = models.URLField()
    vendor_credentials = models.CharField(max_length=255, blank=True, null=True)
    contact_name = models.CharField(max_length=255, blank=True, null=True)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.vendor
