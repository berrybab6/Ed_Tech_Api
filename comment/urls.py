from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/', views.CommentView.as_view()),
    path('reply/<int:pk>/', views.CommentDetail.as_view())
]
