from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import generics, permissions
from .models import Courses
from .serializers import CourseSerializer
from users.models import User

# Create your views here.
def index(request):
    return HttpResponse("Course Page")

class CourseView(generics.GenericAPIView):
    queryset = Courses.objects.all()
    serializer_class = CourseSerializer

    permission_classes = [permissions.IsAuthenticated, ]
    def post(self, request):
        if request.user.admin == True:
            name = request.data.get('name')
            etsc = request.data.get('ETSC')
            teacher_id = request.data.get("teacher_id")
            if name != "" and etsc!=None and teacher_id:
                if etsc >= 1 and etsc <=7:
                    teacher = User.objects.get(id=teacher_id)
                    if teacher and teacher.teacher == True:
                        course = Courses(name=name, ETSC=etsc, teacher=teacher)
                        course.save()
                        ser = CourseSerializer(course)

                        return JsonResponse({"course":ser.data})
                    return JsonResponse({"error":"User Must be a Teacher"})
                else:
                    return JsonResponse({"error":"ETSC must be between 1-7"})
            else:
                return HttpResponse("Course Name should not be empty")
        else:
            return JsonResponse({"error":"UnAuthorized User"})
    def get(self, request):
        if request.user.admin == True:
            course = Courses.objects.all()
            if course:
                ser = CourseSerializer(course, many=True)
                return JsonResponse({"course":ser.data})
            else:
                return HttpResponse("Invalid Request")
        else:
            return JsonResponse({"error":"UnAuthorized User"})
class CourseDetailView(generics.GenericAPIView):
    def put(self, request, pk):
        if request.user.admin == True:
            course = Courses.objects.get(id=pk)
            if course:
                name = request.data.get("name", course.name)
                etsc = request.data.get("ETSC", course.ETSC)
                teacher = request.data.get("teacher_id", course.teacher)
                if name == "":
                    name = course.name
                if etsc is None:
                    etsc = course.ETSC
                is_teacher = User.objects.get(id=teacher)
                if is_teacher and is_teacher.teacher == True:
                    course.name = name
                    course.ETSC = etsc
                    course.teacher = is_teacher
                    course.save()
                    ser = CourseSerializer(course)
                    return JsonResponse({"updated Course":ser.data})
                return JsonResponse({"error":"User must be a Teacher"})
            else:
                return JsonResponse({"error":"No course Found"})
        else:
            return JsonResponse({"error":"UnAuthorized User"})
    def get(self, request, pk):
        course = Courses.objects.get(id=pk)
        if course:
            ser = CourseSerializer(course)
            return JsonResponse({"course":ser.data})

    def delete(self, request, pk):
        if request.user.admin == True:
            course = Courses.objects.get(id=pk)
            if course:
                course.delete()
                return JsonResponse({"message":"Deleted Succesfully"})
            else:
                return JsonResponse({"error":"Course doesnot found"})
        else:
            return JsonResponse({"error":"Unauthorized User"})