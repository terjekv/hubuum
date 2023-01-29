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
    path("users/<val>", views.UserDetail.as_view()),
    path("groups/", views.GroupList.as_view()),
    path("groups/<val>", views.GroupDetail.as_view()),
    #    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #    path('token-auth/', tokens.ObtainExpiringAuthToken.as_view()),
    path("permissions/", views.PermissionList.as_view()),
    path(
        "permissions/<pk>", views.PermissionDetail.as_view(), name="permission-detail"
    ),
    path("namespaces/", views.NamespaceList.as_view()),
    path("namespaces/<val>", views.NamespaceDetail.as_view(), name="namespace-detail"),
    path("namespaces/<val>/groups/", views.NamespaceGroups.as_view()),
    path("hosts/", views.HostList.as_view()),
    path("hosts/<val>", views.HostDetail.as_view(), name="host-detail"),
    path("hosttypes/", views.HostTypeList.as_view()),
    path("hosttypes/<str:pk>", views.HostTypeDetail.as_view(), name="hosttype-detail"),
    path("rooms/", views.RoomList.as_view()),
    path("rooms/<str:pk>", views.RoomDetail.as_view(), name="room-detail"),
    path("jacks/", views.JackList.as_view()),
    path("jacks/<str:pk>", views.JackDetail.as_view(), name="jack-detail"),
    path("persons/", views.PersonList.as_view()),
    path("persons/<str:pk>", views.PersonDetail.as_view(), name="person-detail"),
    path("vendors/", views.VendorList.as_view()),
    path("vendors/<str:pk>", views.VendorDetail.as_view(), name="vendor-detail"),
    path("pos/", views.PurchaseOrderList.as_view()),
    path(
        "pos/<int:pk>",
        views.PurchaseOrderDetail.as_view(),
        name="purchaseorder-detail",
    ),
    path("purchasedocuments/", views.PurchaseDocumentList.as_view()),
    path(
        "purchasedocuments/<int:pk>",
        views.PurchaseDocumentDetail.as_view(),
        name="purchasedocument-detail",
    ),
]
