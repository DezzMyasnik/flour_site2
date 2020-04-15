
"""""
from django.db import models
from django.conf import settings
from django.utils.text import slugify



class Image(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='images_created', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    url = models.URLField()
    #image = models.ImageField(upload_to='images/%Y/%m/%d')
    #description = models.TextField(blank=True)
    show = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True, db_index=True)
    #kitchen_id = models.IntegetField()
    #dishes_id
    #event_id

    class Meta:
        ordering = ('title',)
        verbose_name = 'Галерея'
        verbose_name_plural = 'Галереии'

    def __str__(self):
        return self.title


class ImageGallary(models.Model):
    image = models.ImageField(upload_to='images/%Y/%m/%d', blank=True)
    gallery = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='images', null=True)

    def __str__(self):
        return "%s %s" % (self.gallery, self.image)

    class Meta:
        verbose_name_plural = "images"
"""
from django.db import models

#from taggit.managers import TaggableManager

from photologue.models import Gallery


class GalleryExtended(models.Model):

    # Link back to Photologue's Gallery model.
    gallery = models.OneToOneField(Gallery, related_name='extended', on_delete=models.CASCADE)

    # This is the important bit - where we add in the tags.
    #tags = TaggableManager(blank=True)

    # Boilerplate code to make a prettier display in the admin interface.
    class Meta:
        verbose_name = u'Extra fields'
        verbose_name_plural = u'Extra fields'

    def __str__(self):
        return self.gallery.title
