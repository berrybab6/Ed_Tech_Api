from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import generics, status, permissions
from .serializers import Student_CourseSerializer
from .models import Student
from users.models import User
from users.serializers import UserSerializers
from courses.serializers import CourseSerializer
from courses.models import Courses
# Create your views here.
class StudentCourseView(generics.GenericAPIView):
    queryset = Student.objects.all()
    serializer_class = [Student_CourseSerializer, UserSerializers, CourseSerializer, ]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        student = request.data.get('student', 0)
        course = request.data.get('course', 0)
        if student == 0 or course == 0:
            return JsonResponse({"error":"Please enter the existing Student and Courrse"})
        is_Student = User.objects.get(id=student)
        is_Course = Courses.objects.get(id=course)

        if is_Course and is_Student:
            stud = Student(student=is_Student, course=is_Course)
            stud.save()
            ser_user = UserSerializers(is_Student)
            ser = Student_CourseSerializer(stud)
            return JsonResponse({"message":"Success","student_course":ser.data, "Student_info":ser_user}, status=status.HTTP_201_CREATED)
        return JsonResponse({"error":"specified course or student doesnot exist"})
    def get(self, request):
        stud_course = Student.objects.get(id=1)
        if stud_course:
            is_Student = User.objects.get(id=stud_course.student.id)
            is_Course = Courses.objects.get(id=stud_course.course.id)
            ser_user = UserSerializers(is_Student)
            ser_course = CourseSerializer(is_Course)
            ser = Student_CourseSerializer(stud_course)
            return JsonResponse({"message":"Success","student_course":ser.data, "Student_info":ser_user.data, "course_Info":ser_user.data}, status=status.HTTP_201_CREATED)
