from django.conf.urls import url, include
from .views import GalleryJSONListView, GalleryJSONDitailView



urlpatterns = [
   # url(r'^photolist/$',PhotoJSONListView.as_view(),name='photologue_custom-photo-json-list'),
    url(r'^gallerylist/$', GalleryJSONListView.as_view(),name='photologue_custom-gallery-list'),
    url(r'^gallerylist/(?P<pk>\d+)/$', GalleryJSONDitailView.as_view(), name='photologue_custom-gallery-ditail'),
    #url(r'^imggal$', ImageListView.as_view(), name='subject_list'),
    #url(r'^imggal/(?P<pk>\d+)/$', ImageDetailView.as_view(), name='subject_detail'),
    url(r'^photologue/', include('photologue.urls', namespace='photologue')),
]