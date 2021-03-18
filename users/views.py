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

