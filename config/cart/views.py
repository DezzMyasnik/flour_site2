

from rest_framework.generics import (
    RetrieveUpdateAPIView,
    DestroyAPIView,
    ListAPIView,
)
from rest_framework.response import Response
#rom django.contrib.auth.models import AnonymousUser
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from shop.models import Product
from .models import Cart
from .serializers import CartSerializer
#from .forms import CartAddProductForm
#from cupons.forms import CuponApllyForm



class AddToCartAPIView(APIView):
    """
    Добавление продукта в корзину
    """
    serializer_class = CartSerializer
    #permission_classes = [IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny]
    #permission_classes = [AllowAny,]
    def post(self, request, id):
        self.seission = request.session


        return Response({'message': ['added successfully!']}, status=HTTP_200_OK)

