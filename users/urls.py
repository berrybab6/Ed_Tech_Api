from django.urls import path
from . import views

urlpatterns = [
    path("", views.UserCreateView.as_view(), name="post users"),
    path("<int:pk>/", views.UserDetailView.as_view(), name="User detail"),
    path("userrole/<int:pk>/", views.UserRoleView.as_view(), name="Usr by role"),
    path("login/", views.LoginUserView.as_view(),name="login user")
]
