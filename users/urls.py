from django.urls import path
from . import views

urlpatterns = [
    path("", views.UserCreateView.as_view(), name="post users"),
    path("detail/", views.UserDetailView.as_view(), name="User detail"),
    path("user_role/<int:pk/", views.UserRoleView.as_view(), name="User by role"),
    path("login/", views.LoginUserView.as_view(),name="login user")
]
