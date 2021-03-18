from django.conf.urls import path
from . import views

urlpatterns = [
    path("/", .as_view(), name="")
]
