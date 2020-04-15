from rest_framework.serializers import (
    ModelSerializer,
    ValidationError,
    HyperlinkedIdentityField,
    SerializerMethodField,
)

from shop.models import Product
from .models import Cart
from django.urls import reverse
from django.conf import settings

class CartSerializer(ModelSerializer):
    edit_url = HyperlinkedIdentityField(
        view_name='update_api',
        lookup_field='id',
    )
    delete_url = HyperlinkedIdentityField(
        view_name='delete_api',
        lookup_field='id',
    )

    class Meta:
        model = Cart
        fields = [
            'id',
            'session',
            'product_id',
            'quantity',
            'edit_url',
            'delete_url',
        ]

