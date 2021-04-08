from rest_framework import serializers
from .models import Resources
class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resources
        fields = [
            'id',
            'resource_type',
            'name',
            'category',
            'description',
            'resource_file',
            'created_at',
            'user_id',
        ]
