# from django.shortcuts import render
from rest_framework import generics, permissions, status, response
from django.http import JsonResponse, HttpResponse

from .serializers import ResourceSerializer
from reportlab.pdfgen import canvas
from .models import Resources
from .custom_renderers import VideoRenderer
# Create your views here.
class DisplayResourceFile(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny, ]
    # renderer_classes = [VideoRenderer]

    def get(self, request):
        # renderer_classes = [JPEGRenderer]
        queryset = Resources.objects.get(id=4).resource_file
        data = queryset
        return response.Response(data, content_type='video/mp4')

    def some_view(self, request):
        # Create the HttpResponse object with the appropriate PDF headers.
        response = HttpResponse(content_type='application/pdf')
        queryset = Resources.objects.get(id=1).resource_file
        data = queryset
        response['Content-Disposition'] = '"filename"= data'

        # Create the PDF object, using the response object as its "file."
        p = canvas.Canvas(response)

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        p.drawString(100, 100, "Hello world.")

        # Close the PDF object cleanly, and we're done.
        p.showPage()
        p.save()
        return response

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