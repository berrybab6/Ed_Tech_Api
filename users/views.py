from django.shortcuts import render
from rest_framework import generics, permissions, status
from django.http import JsonResponse
from .models import User
from .serializers import UserSerializers
from django.contrib.auth import login, logout, authenticate

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
        department = request.data.get("department", "")
        if teacher and student:
            return JsonResponse({"error":"User cant be Both Teacher and Student"})
        elif teacher or student:
            user = User.objects.create_user(email=email,
                                            username=username,
                                            password=password,
                                            full_name=full_name,
                                            department=department,
                                            is_student=student,
                                            is_teacher=teacher)

            ser = UserSerializers(user)
            return JsonResponse(ser.data, safe=False)

            # return JsonResponse(){"user":ser.data, "is_teacher":user.is_teacher})
        else:
            return JsonResponse({"error":"Please choose one role"})
    def get(self, request):
        user = User.objects.all()
        ser = UserSerializers(user, many=True)
        return JsonResponse({"users":ser.data})
class LoginUserView(generics.GenericAPIView):
    
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = [permissions.AllowAny, ]
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        if email == "" or password == "":
            return JsonResponse({"msg":"Empty Field"}, status=status.HTTP_404_NOT_FOUND)
        user = authenticate(email=email, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                # token, created = Token.objects.get_or_create(user=user)

                ser = UserSerializers(user)
                # return JsonResponse({"message":"user logged in succesfully", "user":ser.data})
                return JsonResponse(ser.data, safe=False, status=status.HTTP_201_CREATED)
            
            return JsonResponse({"error":"disabled account"}, status=status.HTTP_404_NOT_FOUND)
            #Return a 'disabled account' error message
        else:
            return JsonResponse({"error":"invalid login"}, status=status.HTTP_204_NO_CONTENT)
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
        if pk in range(0, 5):
            if pk == 0:
                user = User.objects.filter(admin=True)
                # ser = UserSerializers(user, many=True)
            if pk == 1:
                user = User.objects.filter(teacher=True)
                # ser = UserSerializers(user, many=True)
            if pk == 2:
                user = User.objects.filter(student=True)
                # ser = UserSerializers(user, many=True)
            if pk == 3:
                user = User.objects.filter(staff=True)
            # ser = UserSerializers(user, many=True)
            if pk == 4:
                user = User.objects.filter(active=True)
            ser = UserSerializers(user, many=True)
            return JsonResponse(ser.data, safe=False)
        else:
            return JsonResponse({"error":"There is no User with this role"})