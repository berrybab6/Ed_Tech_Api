"""REsources urls
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


urlpatterns = [
    # path('', views.CreateResourceView.as_view()),
    # path("files/", views.DisplayResourceFile.as_view())
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

