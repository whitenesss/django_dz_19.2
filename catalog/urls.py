from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import home
from catalog.views import contact

app_name = CatalogConfig.name

urlpatterns = [
    path("", home, name="index"),
    path("contact/", contact, name="contact")]
