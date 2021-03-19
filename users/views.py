from django.shortcuts import render
from rest_framework import generics, permissions
from django.http import JsonResponse
from .models import User
from .serializers import UserSerializers

# Create your views here.
class UserCreateView(generics.GenericAPIView):
    serializer_class = UserSerializers
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny, ]

    def post(self, request):
        email = request.data.get("email", "")
        password = request.data.get("password", "")
        student = request.data.get("student", False)
        teacher = request.data.get("teacher", False)
        full_name = request.data.get("full_name", "")
        user = User.objects.create_user(email=email, full_name=full_name, password=password, is_student=student, is_teacher=teacher)
        ser = UserSerializers(user)
        return JsonResponse({"user":ser.data})