from photologue.views import PhotoListView, GalleryListView
from rest_framework import mixins
from rest_framework import generics
#from braces.views import JSONResponseMixin
from photologue.models import Gallery
from .serializers import GallerySerializer



class GalleryJSONListView(generics.ListAPIView):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer

class GalleryJSONDitailView(generics.RetrieveAPIView):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer



