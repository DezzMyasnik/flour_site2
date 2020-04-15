from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='blog_posts', on_delete=models.CASCADE)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')


    def get_absolute_url(self):
        return "/feed/%s/" % self.slug

class Meta:
    ordering = ('-publish',)
    verbose_name = "Публикация"
    verbose_name_plural = "Публикации"

def __str__(self):
    return self.title
