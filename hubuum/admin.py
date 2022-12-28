from django.contrib import admin
from .models import *

myModels = [Host, HostType, Person, Room, Jack, Vendor, DetectedHostData, ExternalSource, PurchaseOrder, PurchaseDocuments]
admin.site.register(myModels)