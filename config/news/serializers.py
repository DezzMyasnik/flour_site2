from rest_framework import serializers
from .models import Post


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'author', 'body', 'publish')