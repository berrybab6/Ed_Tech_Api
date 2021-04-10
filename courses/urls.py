from django.urls import path
from . import views
urlpatterns = [
    path('', views.CourseView.as_view(), name="course view"),
    path('<int:pk>', views.CourseDetailView.as_view(), name="Course Detail view")
]
