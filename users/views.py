from django.shortcuts import render
from rest_framework import generics, permissions, status
from django.http import JsonResponse
from .models import User
from django.contrib.auth.hashers import make_password,check_password

from .serializers import UserSerializers
from django.contrib.auth import login, logout, authenticate

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from wsgiref.util import FileWrapper
from .custom_renderers import JPEGRenderer, PNGRenderer
from rest_framework import generics

from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import renderers
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.decorators import renderer_classes, api_view
from rest_framework.renderers import StaticHTMLRenderer
from django.http import HttpResponse
from PIL import Image


class ImageAPIView(generics.RetrieveAPIView):

    queryset = User.objects.all()
    renderer_classes = [JPEGRenderer]

    def get(self, request, pk):
        # renderer_classes = [JPEGRenderer]
        queryset = User.objects.get(username=pk).profile_url
        data = queryset
        return Response(data, content_type='image/jpg')


class ImageRelated(generics.GenericAPIView):
    serializer_class = UserSerializers
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny, ]

    def get(self,request):
        user = User.objects.get(id=7)
        if user:
            picture = user.profile_url
            return JsonResponse(picture, safe=False)


# Create your views here.
class ChangePassword(generics.GenericAPIView):
    serializer_class = UserSerializers
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]

    """Change Password
    """
    def put(self, request):
        user = User.objects.get(id=request.user.id)
        if user:
            oldpass = request.data.get("password","")
            newpass = request.data.get('newpassword',"")

            if oldpass and newpass:
                password = user.password
                if check_password(oldpass, password):
                    user.set_password(newpass)
                    user.save()
                    return JsonResponse({"message":"Password Changed Succesfully"}, status=status.HTTP_201_CREATED)
            else:
                return JsonResponse({"message":"password and new password fields required"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({"message":"user Doesnot Found"}, status=status.HTTP_404_NOT_FOUND)
class UserCreateView(generics.GenericAPIView):
    serializer_class = UserSerializers
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]


    def post(self, request):
        if request.user.admin:
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
                # return JsonResponse(ser.data, safe=False)

                return JsonResponse({"user":ser.data, "is_teacher":user.is_teacher})
            else:
                return JsonResponse({"error":"Please choose one role"})
        else:
            return JsonResponse(
                                {"error":"you are not authorized to add user"},
                                status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request):
        if request.user.admin:
            user = User.objects.all()
            if user:
                ser = UserSerializers(user, many=True)
                return JsonResponse({"users":ser.data})
            else:
                return JsonResponse({"error":"User doesnot exist"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return JsonResponse({"error":"User UnAuthorized to view users"}, status=status.HTTP_401_UNAUTHORIZED)
class LoginUserView(ObtainAuthToken):

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
                token, created = Token.objects.get_or_create(user=user)

                ser = UserSerializers(user)
                # return JsonResponse({"message":"user logged in succesfully", "user":ser.data})

                # return JsonResponse(ser.data, safe=False)
                return JsonResponse({"user":ser.data, "token":token.key}, status=status.HTTP_201_CREATED)

            return JsonResponse({"error":"disabled account"}, status=status.HTTP_404_NOT_FOUND)
            #Return a 'disabled account' error message
        else:
            return JsonResponse({"error":"invalid login"}, status=status.HTTP_400_BAD_REQUEST)
class UserDetailView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = [permissions.AllowAny, ]
    def get(self, request):
        user = User.objects.get(id=request.user.id)
        if user:
            ser = UserSerializers(user)
            return JsonResponse({"user_detail":ser.data}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error":"User Doesnot exist"}, status=status.HTTP_404_NOT_FOUND)
    def put(self, request):
        user = User.objects.get(id=7)
        if user:
            username = request.data.get('username', user.username)
            userprofile = request.data.get('profile_url', user.profile_url)

            full_name = request.data.get('full_name', user.full_name)
            user.username = username
            user.profile_url = userprofile
            user.full_name = full_name
            try:
                user.save()
                ser = UserSerializers(user)
                return JsonResponse({"updated user":ser.data}, status=status.HTTP_201_CREATED)
            except Exception:
                return JsonResponse({"error":"Update Failed"})
        else:
            return JsonResponse({"error":"User doesnot exist"})
    def delete(self, request):
        user = User.objects.get(id=request.user.id)
        if user:
            user.delete()
            return JsonResponse({"success":"User Deleted Succesfully"}, status=status.HTTP_204_NO_CONTENT)
class UserRoleView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, pk):
        if request.user.admin:
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
        else:
            return JsonResponse({"error":"Admin Only"}, status=status.HTTP_401_UNAUTHORIZED)

