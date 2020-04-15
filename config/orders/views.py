from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic.base import RedirectView
from rest_framework.generics import (
    RetrieveUpdateAPIView,
    DestroyAPIView,
    ListAPIView,
)


from django.contrib.sessions.models import Session
from django.contrib.auth.models import AnonymousUser
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny


from .serializers import (
    OrdersSerializer,
    CartSerializer,
    OrderUpdateSerializer,
)
from acounts.models import Accounts
from shop.models import Product
from .models import Checkout
from .form import BankForm
from .permissions import IsOwnerOrReadOnly
from rest_framework import status,viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response
import requests
from django.conf import settings
import time
#import urllib2,urllib

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def bank_pocessing(request, *args, **kwargs):


    query_params_copy = request.query_params.copy()
    # This is just some adjustments to make the legacy request params work with the serializer
    query_params_copy['type'] = request.query_params.get("type", None)
    query_params_copy['id'] = request.query_params.get("id", None)

    query_params_copy["descr"] = request.query_params.get("descr", None)
    query_params_copy["date"] = request.query_params.get("date", None)
    query_params_copy['result'] = request.query_params.get("result", None)
    query_params_copy['amt'] = request.query_params.get("amt", None)
    query_params_copy['comment'] = request.query_params.get("comment", None)
    query_params_copy['fn'] = request.query_params.get("fn", None)
    query_params_copy['ln'] = request.query_params.get("ln", None)
    query_params_copy['phone'] = request.query_params.get("phone", None)
    query_params_copy['email'] = request.query_params.get("email",None)


    #print(query_params_copy['descr'])
    if query_params_copy['result'] == '0':
        qs = Checkout.objects.filter(reciept=query_params_copy["descr"])
        if qs.exists():
            total_price = 0.0
            for order in qs:
                print(order.status)
                if order.status == 'pending':
                    order.status = 'accepted'
                    total_price = total_price + order.price
                    order.additional_info = "{} {}\n" \
                                            "tel: {}\n" \
                                            "emali:{}".format(query_params_copy['fn'],query_params_copy['ln'],
                                                        query_params_copy['phone'], query_params_copy['email'] )
                    order.save()
                    if query_params_copy['amt'] == total_price:
                        return Response('RESP_CODE=0', status=HTTP_200_OK)
                elif order.status == 'accepted':
                    return Response('RESP_CODE=1', status=HTTP_200_OK)


    #else:
     #   return Response({'message': ['Проблема: {}'.format(query_params_copy['comment'])]}, status=HTTP_200_OK)

    return Response('RESP_CODE=-1', status=HTTP_200_OK)





def page(request):
    data = {
        'PurchaseAmt': 10,
        'PurchaseDesc': 'TestPurchasel',
        'CountryCode': 643,
        'CurrencyCode': 643,
        'MerchantName': 'TestMerchant',
        'MerchantURL': 'https://www.merchantURL.ru',
        'MerchantCity': 'MOSCOW',
        'MerchantID': '000001680997001-80997001'

    }
    url = 'https://e-commerce.raiffeisen.ru/vsmc3ds/pay_check/3dsproxy_init.jsp'
    r = requests.post(url,data=data,json=None)
    return Response(r.content)

class AddToCartAPIView(APIView):
    """
    Добавление продукта в карзину
    """
    #permission_classes = [IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny]
    permission_classes = [AllowAny,]
    def post(self, request, id):
        user = self.request.user
        if user.is_authenticated:
            qs = Checkout.objects.filter(product_id=id, user=user, status='waiting')
            if qs.exists():
                return Response({'message': ['already exists!']}, status=HTTP_200_OK)
            else:
                product = Product.objects.filter(id=id, available=True).first()
                checkout = Checkout.objects.create(
                    user=self.request.user,
					session_key=self.request.session.session_key,
                    product_id=product,
                    name=product.name,
                    slug=product.slug,
                    price=product.price,
                    quantity=1,
                    #discount=product.discount,
                    image=product.image,
                )
                return Response({'message': ['added successfully!']}, status=HTTP_200_OK)
        else:
            if not request.session.exists(request.session.session_key):
                request.session.create()
            

            qs = Checkout.objects.filter(product_id=id, session_key=self.request.session.session_key, status='waiting')
            #print(self.request.session.session_key)
            if qs.exists():
                return Response({'message': ['already exists!']}, status=HTTP_200_OK)
            #user_=AnonymousUser.
            else:
                product = Product.objects.filter(id=id, available=True).first()
                checkout = Checkout.objects.create(
                    session_key=self.request.session.session_key,
                    product_id=product,
                    name=product.name,
                    slug=product.slug,
                    price=product.price,
                    quantity=1,
                    #discount=product.discount,
                    image=product.image,
                )
                return Response({'message': ['added successfully!']}, status=HTTP_200_OK)

            #return Response({'message': ['you must be logged in first!']}, status=HTTP_200_OK)


class CartAPIView(ListAPIView):
    """
    Просмотр карзины покупок
    """
    serializer_class = CartSerializer
    #permission_classes = [AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated,]
    permission_classes = [AllowAny,]
    def get_queryset(self, *args, **kwargs):
        queryset = Checkout.objects.filter(session_key=self.request.session.session_key, status='waiting').order_by('-id')

        return queryset


class PendingOrdersAPIView(ListAPIView):
    serializer_class = OrdersSerializer
    #permission_classes = [IsAuthenticatedOrReadOnly, IsAuthenticated]
    permission_classes = [AllowAny, ]
    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated:
            queryset = Checkout.objects.filter(user=self.request.user, status='pending').order_by('-id')
        else:
            queryset = Checkout.objects.filter(session_key=self.request.session.session_key, status='pending')\
                .order_by('-id')

        return queryset


class AcceptedOrdersAPIView(ListAPIView):
    serializer_class = OrdersSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        queryset = Checkout.objects.filter(user=self.request.user, status='accepted').order_by('-id')
        return queryset


class RejectedOrdersAPIView(ListAPIView):
    serializer_class = OrdersSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        queryset = Checkout.objects.filter(user=self.request.user, status='rejected').order_by('-id')
        return queryset


class OrderUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = OrderUpdateSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
    #permission_classes = [AllowAny, IsOwnerOrReadOnly, IsAuthenticated]
    permission_classes = [AllowAny, ]
    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated:
            queryset = Checkout.objects.filter(user=self.request.user, status='waiting').order_by('-id')
        else:
            queryset = Checkout.objects.filter(session_key=self.request.session.session_key, status='waiting').order_by(
                '-id')

        return queryset


class OrderDeleteAPIView(DestroyAPIView):
    serializer_class = OrdersSerializer
    lookup_field = 'id'
    #permission_classes = [AllowAny, IsOwnerOrReadOnly, IsAuthenticated]
    permission_classes = [AllowAny, ]
    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated:
            queryset = Checkout.objects.filter(user=self.request.user, status='waiting', id=self.kwargs['id']).order_by('-id')
        else:
            queryset = Checkout.objects.filter(session_key=self.request.session.session_key, status='waiting', id=self.kwargs['id']).order_by(
                '-id')

        return queryset

def gen_reciept_num():
    from random import randint

    reciept_final = 100000 + randint(100001, 200000)
    list_rep = Checkout.objects.values('reciept')
    #print(list_rep)
    reciept_final = {'reciept': reciept_final}
    while reciept_final in list_rep:

        reciept_final = {'reciept': 100000 + randint(100001, 200000)}

    #print(reciept_final['reciept'])
    return reciept_final['reciept']

class BuyOrdersPostView(APIView):
    lookup_field = 'id'
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated,]

    def post(self, request):
        username = self.request.user
        #print(username)
        if username is None:
            raise Response({'message': ['you have not the permission to do that!']}, status=HTTP_400_BAD_REQUEST)
        else:
            account = Accounts.objects.filter(user=username)
            #print(account)
            qs = Checkout.objects.filter(user=username, status='waiting')
            #print(qs.exists())
            if account.exists():
                user = account.first()
                if user.email is None:
                    return Response(
                        {'message': ['add your information first to complete buy orders!']},
                        status=HTTP_200_OK
                    )

            if qs.exists():
                total_price = 0.0
                reciept_final = gen_reciept_num()
                for order in qs:

                    order.status = 'pending'
                    order.session_key = self.request.session.session_key
                    order.reciept = reciept_final
                    total_price = total_price + order.price
                    #print(total_price)
                    order.save()
                    product = Product.objects.filter(id=order.product_id).first()
                    product.quantity -= order.quantity

                    product.save()

                data = {
                    'PurchaseAmt': total_price,
                    'PurchaseDesc': reciept_final,
                    'CountryCode': 643,
                    'CurrencyCode': 643,
                    'MerchantName': 'CSM Ltd',
                    'MerchantURL': 'https://studiomyka.ru/home',
                    'MerchantCity': 'MOSKVA',
                    'MerchantID': '000001788599001-88599001',
                    'SuccessURL': 'https://studiomyka.ru/orders/buy/success',
                    'FailURL': 'https://studiomyka.ru/orders/buy/success',
                    'CardholderName': 'Y',
                    'Email': 'Y',
                    'Phone': 'Y',

                }
                userform = BankForm(data)

                return render(request, "test.html", {"form": userform.as_p()})




class BuyOrdersAPIView(APIView):
    lookup_field = 'id'
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated,]

    def post(self, request):
        username = self.request.user
        #print(username)
        if username is None:
            raise Response({'message': ['you have not the permission to do that!']}, status=HTTP_400_BAD_REQUEST)
        else:
            account = Accounts.objects.filter(user=username)
            #print(account)
            qs = Checkout.objects.filter(user=username, status='waiting')
            #print(qs.exists())
            if account.exists():
                user = account.first()
                if user.email is None:
                    return Response(
                        {'message': ['add your information first to complete buy orders!']},
                        status=HTTP_200_OK
                    )

            if qs.exists():
                total_price = 0.0
                reciept_final = gen_reciept_num()
                for order in qs:

                    order.status = 'pending'
                    order.session_key = self.request.session.session_key
                    order.reciept = reciept_final
                    total_price = total_price + order.price
                    #print(total_price)
                    order.save()
                    product = Product.objects.filter(id=order.product_id).first()
                    product.quantity -= order.quantity

                    product.save()

                data = {
                    'ActionURL': settings.ACTION_URL,
                    'PurchaseAmt': total_price,
                    'PurchaseDesc': reciept_final,
                    'CountryCode': 643,
                    'CurrencyCode': 643,
                    'MerchantName': 'CSM Ltd',
                    'MerchantURL': 'https://studiomyka.ru/home',
                    'MerchantCity': 'MOSKVA',
                    'MerchantID': '000001788599001-88599001',
                    'SuccessURL': 'https://studiomyka.ru/orders/buy/success',
                    'FailURL': 'https://studiomyka.ru/orders/buy/success',
                    'CardholderName': 'Y',
                    'Email': 'Y',
                    'Phone': 'Y',

                }
                #userform = BankForm(data)

                return Response(
                    data,
                    status=HTTP_200_OK
                )






