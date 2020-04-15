from rest_framework import serializers
from .models import GalleryExtended
from photologue.models import Gallery, Photo

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Photo
        fields = ['id', 'image',]

class GallerySerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True)
    class Meta:
        model = Gallery
        fields = ['id', "title", "slug", "photos"]
        depth = 3