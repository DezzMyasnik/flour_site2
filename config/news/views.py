from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from .serializers import NewsSerializer
import django_filters.rest_framework
from django_filters import rest_framework as filters
# Create your views here.
from .models import Post


class NewsListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = NewsSerializer


class NewsFilter(filters.FilterSet):
    """

    """
    publish__gte = filters.DateTimeFilter(field_name="publish", lookup_expr='gte')
    publish__lt = filters.DateTimeFilter(field_name="publish", lookup_expr='lte')

    class Meta:
        model = Post
        fields = ['status']

class CustomNewsView(generics.ListAPIView):
    """
    Выбор новостей по параметрам
    формат строки запроса: ?publish__gte=08.10.2019&publish__lt=10.10.2019&status=published

    """
    serializer_class = NewsSerializer
    queryset = Post.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = NewsFilter


class NewsDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = NewsSerializer