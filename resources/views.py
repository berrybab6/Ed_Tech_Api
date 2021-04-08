# from django.shortcuts import render
from rest_framework import generics, permissions, status
from django.http import JsonResponse
from .serializers import ResourceSerializer
from .models import Resources
# Create your views here.
class CreateResourceView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = ResourceSerializer
    queryset = Resources.objects.all()

    def post(self, request):
        if request.user:
            name = request.data['name']
            description = request.data.get('description', "")
            resource_file = request.FILES.get('resource_file', "")
            category = request.data.get('category', 8)
            # created = request.data.get('created', dt.now())
            resource_type = request.data.get('resource_type', 6)
            # user_id = request.data['user_id']
            try:
                resource = Resources(name=name, description=description, category=category, user=request.user, resource_type=resource_type, resource_file=resource_file)
                resource.save()
                ser = ResourceSerializer(resource)
                return JsonResponse({'resource':ser.data}, status=status.HTTP_201_CREATED)
            except Exception:
                raise ValueError("Invalid request")
    def get(self, request):
        resources = Resources.objects.all()
        if resources:
            ser = ResourceSerializer(resources, many=True)
            return JsonResponse({"resources":ser.data})
        else:
            return JsonResponse({"error":"Resources doesnot exist"}, status=status.HTTP_404_NOT_FOUND)