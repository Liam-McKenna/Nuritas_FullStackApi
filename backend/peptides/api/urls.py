from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from peptides.api import views

# Create a router and register our viewsets with it.
router = DefaultRouter()

router.register(r"users", views.UserViewSet, basename="user")
router.register(r"peptides", views.PeptideViewSet, basename="peptide")
router.register(r"assays", views.AssayViewSet, basename="assay")


# The API URLs are now determined automatically by the router.
urlpatterns = [
    url(r"^", include(router.urls)),
]
