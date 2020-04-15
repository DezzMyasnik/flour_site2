'''
from django.contrib import admin
from .models import Image, ImageGallary

class ImageInline(admin.TabularInline):
    fk_name = 'gallery'
    model = ImageGallary

class ImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'created']
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ['created']
    inlines = [ImageInline, ]


admin.site.register(Image, ImageAdmin)

'''

from django.contrib import admin

from photologue.admin import GalleryAdmin as GalleryAdminDefault
from photologue.models import Gallery
from .models import GalleryExtended


class GalleryExtendedInline(admin.StackedInline):
    model = GalleryExtended
    can_delete = False


class GalleryAdmin(GalleryAdminDefault):

    class Meta:
        model = Gallery
    """Define our new one-to-one model as an inline of Photologue's Gallery model."""

    #inlines = [GalleryExtendedInline, ]

admin.site.unregister(Gallery)
admin.site.register(Gallery, GalleryAdmin)


