from django.conf.urls import url
from django.views.static import serve
from . import views


urlpatterns = [
    url(r'^$', views.ProductListView.as_view(), name='subject_list'),
    url(r'^(?P<pk>\d+)/$', views.ProductsDetailView.as_view(), name='subject_detail'),
    url(r'^filter/$', views.ProductList.as_view(), name='filter_list'),
    url(r'^filter/kitchen/$', views.KitchenFromProducts.as_view(), name='kitchen_list'),

    url(r'^dishes/$', views.DishesListView.as_view(), name='dishes_list'),
    url(r'^dishes/(?P<pk>\d+)/$', views.DishesDetailView.as_view(), name='dish_detail'),
    #
    url(r'^kitchen/$', views.KitchenListView.as_view(), name='subject_list'),
    url(r'^kitchen/(?P<pk>\d+)/$', views.KitchenDetailView.as_view(), name='subject_detail'),
    #

]