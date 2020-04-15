from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings
from shop.models import Product
from django.core.validators import RegexValidator


#User = get_user_model()
User = settings.AUTH_USER_MODEL
"""
class Acquairing(models.Model):
    data = {
        'PurchaseAmt': order.price,
        'PurchaseDesc': '432425235523',
        'CountryCode': 643,
        'CurrencyCode': 643,
        'MerchantName': 'CSM Ltd',
        'MerchantURL': 'https://studiomyka.ru/home',
        'MerchantCity': 'MOSKVA',
        'MerchantID': '000001780599001-80599001'

    }
"""
class Checkout(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'Waiting'),
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,verbose_name=u"Пользователь" )
    session_key = models.CharField(max_length=200, default='foo')
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='waiting')
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="ID мероприятия")
    name = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, null=True)
    price = models.FloatField(default=0, blank=True, null=True)
    quantity = models.PositiveIntegerField()
    discount = models.FloatField(default=0, blank=True, null=True)
    image = models.ImageField()
    reciept = models.PositiveIntegerField(blank=True, default=100)

    email = models.EmailField(max_length=255, verbose_name='Email', blank=True)
    first_name = models.CharField(max_length=255, verbose_name="Имя заказчика",blank=True)
    last_name = models.CharField(max_length=255, verbose_name="Фамилия заказчика", blank=True, default='')

    # phone_number1 = PhoneNumberField(blank=True, null=True, verbose_name=u"Телефон", region="RU")
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Телефон должен быть в формате: '+79999999999'. ")
    phone_number1 = models.CharField(validators=[phone_regex], max_length=16, blank=True, verbose_name="Телефон")
    additional_info = models.TextField(blank=True, null=True)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    #REQUIRED_FIELDS = ['first_name', 'phone_number1', 'email', ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = 'Заказы'