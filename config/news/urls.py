
from django.conf.urls import url
from . import views
from .feeds import LatestPostsFeed

urlpatterns = [
    url(r'^$', views.NewsListView.as_view(), name='subject_list'),
    url(r'^(?P<pk>\d+)/$', views.NewsDetailView.as_view(), name='subject_detail'),
    url(r'^filter/$', views.CustomNewsView.as_view(), name='filter_list'),
    url(r'^feed/$', LatestPostsFeed(), name='post_feed'),
]