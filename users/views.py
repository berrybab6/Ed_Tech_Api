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
        email = request.data.get("email")
        password = request.data.get("password", "")
        student = request.data.get("student", False)
        teacher = request.data.get("teacher", False)
        full_name = request.data.get("full_name", "")
        username = request.data.get("username")
        if teacher == True and student == True:
            return JsonResponse({"error":"User cant be Both Teacher and Student"})
        elif teacher == True or student == True:
            user = User.objects.create_user(email=email, username=username, password=password, full_name=full_name, is_student=student, is_teacher=teacher)

            ser = UserSerializers(user)
            return JsonResponse({"user":ser.data, "is_teacher":user.is_teacher})
        else:
            return JsonResponse({"error":"Please choose one role"})
    def get(self, request):
        user = User.objects.all()
        ser = UserSerializers(user, many=True)
        return JsonResponse({"users":ser.data})
class UserDetailView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = [permissions.AllowAny, ]
    def get(self, request, pk):
        user = User.objects.get(id=pk)
        ser = UserSerializers(user)
        return JsonResponse({"user_detail":ser.data})
class UserRoleView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = [permissions.AllowAny, ]

    def get(self, request, pk):
        if pk in range(0,5):
            if pk == 0:
                user = User.objects.filter(admin = True)
                # ser = UserSerializers(user, many=True)
            if pk == 1:
                user = User.objects.filter(teacher = True)
                # ser = UserSerializers(user, many=True)
            if pk == 2:
                user = User.objects.filter(student = True)
                # ser = UserSerializers(user, many=True)
            if pk == 3:
                user = User.objects.filter(staff = True)
            # ser = UserSerializers(user, many=True)
            if pk == 4:
                user = User.objects.filter(active = True)
            ser = UserSerializers(user, many=True)
            return JsonResponse({"user":ser.data})
        else:
            return JsonResponse({"error":"There is no User with this role"})