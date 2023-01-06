"""Set up the admin site with the models we want to allow access to."""

from django.contrib import admin
from .models import (
    Host,
    HostType,
    Person,
    Room,
    Jack,
    Vendor,
    PurchaseOrder,
    PurchaseDocuments,
)

models = [
    Host,
    HostType,
    Person,
    Room,
    Jack,
    Vendor,
    PurchaseOrder,
    PurchaseDocuments,
]
admin.site.register(models)
