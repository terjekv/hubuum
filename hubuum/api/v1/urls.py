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
    path("users/", views.UserList.as_view()),
    path("user/<lookup_value>", views.UserDetail.as_view()),
    path("groups/", views.GroupList.as_view()),
    path("group/<lookup_value>", views.GroupDetail.as_view()),
    #    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #    path('token-auth/', tokens.ObtainExpiringAuthToken.as_view()),
    path("namespaces/", views.NamespaceList.as_view()),
    path(
        "namespace/<lookup_value>", views.Namespace.as_view(), name="namespace-detail"
    ),
    path("hosts/", views.HostList.as_view()),
    path("host/<lookup_value>", views.Host.as_view(), name="host-detail"),
    #    path("externals", views.ExternalSourceList.as_view()),
    #    path(
    #        "external/<int:pk>",
    #        views.ExternalSource.as_view(),
    #        name="externals-detail",
    #    ),
    path("hosttypes/", views.HostTypeList.as_view()),
    path("hosttype/<str:pk>", views.HostType.as_view(), name="hosttype-detail"),
    path("rooms/", views.RoomList.as_view()),
    path("room/<str:pk>", views.Room.as_view(), name="room-detail"),
    path("jacks/", views.JackList.as_view()),
    path("jack/<str:pk>", views.Jack.as_view(), name="jack-detail"),
    path("persons/", views.PersonList.as_view()),
    path("person/<str:pk>", views.Person.as_view(), name="person-detail"),
    path("vendors/", views.VendorList.as_view()),
    path("vendor/<str:pk>", views.Vendor.as_view(), name="vendor-detail"),
    path("pos/", views.PurchaseDocumentList.as_view()),
    path(
        "po/<int:pk>",
        views.PurchaseDocument.as_view(),
        name="purchaseorder-detail",
    ),
    path("purchasedocuments/", views.PurchaseDocumentList.as_view()),
    path(
        "purchasedocument/<int:pk>",
        views.PurchaseDocument.as_view(),
        name="purchasedocument-detail",
    ),
]
