"""Versioned (v1) URLs for hubuum."""

from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
# router.register(r'host', views.HeroViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
    path("api/v1/users/", views.UserList.as_view()),
    path("api/v1/user/<lookup_value>", views.UserDetail.as_view()),
    path("api/v1/groups/", views.GroupList.as_view()),
    path("api/v1/group/<lookup_value>", views.GroupDetail.as_view()),
    #    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #    path('api/v1/token-auth/', tokens.ObtainExpiringAuthToken.as_view()),
    path("api/v1/hosts/", views.HostList.as_view()),
    path("api/v1/host/<lookup_value>", views.Host.as_view(), name="host-detail"),
    #    path("api/v1/externals", views.ExternalSourceList.as_view()),
    #    path(
    #        "api/v1/external/<int:pk>",
    #        views.ExternalSource.as_view(),
    #        name="externals-detail",
    #    ),
    path("api/v1/hosttypes/", views.HostTypeList.as_view()),
    path("api/v1/hosttype/<str:pk>", views.HostType.as_view(), name="hosttype-detail"),
    path("api/v1/rooms/", views.RoomList.as_view()),
    path("api/v1/room/<str:pk>", views.Room.as_view(), name="room-detail"),
    path("api/v1/jacks/", views.JackList.as_view()),
    path("api/v1/jack/<str:pk>", views.Jack.as_view(), name="jack-detail"),
    path("api/v1/persons/", views.PersonList.as_view()),
    path("api/v1/person/<str:pk>", views.Person.as_view(), name="person-detail"),
    path("api/v1/vendors/", views.VendorList.as_view()),
    path("api/v1/vendor/<str:pk>", views.Vendor.as_view(), name="vendor-detail"),
    path("api/v1/pos/", views.PurchaseDocumentList.as_view()),
    path(
        "api/v1/po/<int:pk>",
        views.PurchaseDocument.as_view(),
        name="purchaseorder-detail",
    ),
    path("api/v1/purchasedocuments/", views.PurchaseDocumentList.as_view()),
    path(
        "api/v1/purchasedocument/<int:pk>",
        views.PurchaseDocument.as_view(),
        name="purchasedocument-detail",
    ),
]
