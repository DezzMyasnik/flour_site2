from rest_framework import generics
from .serializers import ProductSerializer, \
    DishesSerializer, \
    KitchenSerializer, \
    DishFormatSerializer,\
    KitchenFromProductsSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters

# Create your views here.
from .models import Product, Dishes,Kitchen, DishFormat, DishesGallary




class ProductFilter(filters.FilterSet):
    """

    """
    dateofevent__gte = filters.DateTimeFilter(field_name="dateofevent", lookup_expr='gte')
    dateofevent__lt = filters.DateTimeFilter(field_name="dateofevent", lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['available']

class KitchenFromProducts(generics.ListAPIView):
    queryset = Product.objects.values('kitchen').distinct()
    serializer_class = KitchenFromProductsSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductFilter






class ProductList(generics.ListAPIView):
    """
        Выборка продукта по значению полей Avalible и дата времени проведения
        Формат строки запроса
        /product/filter/?dateofevent__gte=2019-08-06&dateofevent__lt=2019-08-14&available=True
        Ответ представляетс собой список обектов, соответсующей структуры

    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductFilter



class ProductListView(generics.ListAPIView):
    """
    Получение списка всех продуктов
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductsDetailView(generics.RetrieveAPIView):
    """
    Получение детальной информации по отдельнопу продукту
    /product/<id>
    Результат: объект модели
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class DishesListView(generics.ListAPIView):
    """
    Получение списка всех блюд.
    Запрос: /product/dishes/
    Результат: список объектов содели Dishes
    """
    queryset = Dishes.objects.all()
    serializer_class = DishesSerializer

class DishesDetailView(generics.RetrieveAPIView):
    """
        Получение списка всех блюд.
        Запрос /product/dishes/<id>
        Результат: список объектов модели Dishes

    """
    queryset = Dishes.objects.all()
    serializer_class = DishesSerializer


class DishFormatView(generics.RetrieveAPIView):
    """
        Структура позволяющая опеределить порядок приготовления блюд в процессе мастер класса
    """
    queryset = DishFormat.objects.all()
    serializer_class = DishFormatSerializer

class KitchenListView(generics.ListAPIView):
    """
            Получение списка всех кухонь.
            Запрос /product/kitchen
            Результат: список объектов модели Kitchen

        """
    queryset = Kitchen.objects.all()
    serializer_class = KitchenSerializer

class KitchenDetailView(generics.RetrieveAPIView):
    """
            Получение детализации категории кухни.
            Запрос /product/kitchen/<id>
            Результат: список объектов модели Kitchcen

        """
    queryset = Kitchen.objects.all()
    serializer_class = KitchenSerializer