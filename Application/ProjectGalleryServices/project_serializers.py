from rest_framework import serializers

from .project_models import (
    ProjectImages,
    Project,
    Gallery
)


class ProjectImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImages
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    images = ProjectImagesSerializer(many=True, read_only=True)
    class Meta:
        model = Project
        fields = '__all__'


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = '__all__'