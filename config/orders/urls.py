from django.conf.urls import url
from django.views.generic.base import RedirectView
from .views import (
    AddToCartAPIView,
    CartAPIView,
    OrderUpdateAPIView,
    OrderDeleteAPIView,
    PendingOrdersAPIView,
    AcceptedOrdersAPIView,
    RejectedOrdersAPIView,
    BuyOrdersAPIView,
    BuyOrdersPostView,

)
from .views import bank_pocessing

urlpatterns = [
    url(r'^order/(?P<id>\d+)/$', AddToCartAPIView.as_view(), name='order_api'),
    url(r'^order/(?P<id>\d+)/update/$', OrderUpdateAPIView.as_view(), name='update_api'),
    url(r'^order/(?P<id>\d+)/delete/$', OrderDeleteAPIView.as_view(), name='delete_api'),
    url(r'^cart/$', CartAPIView.as_view(), name='cart_api'),
    url(r'^pending/$', PendingOrdersAPIView.as_view(), name='pending_api'),
    url(r'^rejected/$', RejectedOrdersAPIView.as_view(), name='rejected_api'),
    url(r'^accepted/$', AcceptedOrdersAPIView.as_view(), name='accepted_api'),
    url(r'^buy/$', BuyOrdersAPIView.as_view(), name='buy_api'),
    url(r'^buywithpost/$', BuyOrdersPostView.as_view(), name='buy_post'),
    url(r'^bank_process/$', bank_pocessing),
    #url(r'^page/$',page),
    #url(r'^snipet/$', entry_ViewSet.as_view({'post':'list'}))
]