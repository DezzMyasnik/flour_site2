from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from shop.models import Product
#rom phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import RegexValidator

# Create your models here.


class ActivForm(models.Model):
    email = models.EmailField(max_length=255, verbose_name='Email')
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=u"ID мероприятия")
    first_name = models.CharField(max_length=255, verbose_name="Имя заказчика")
    last_name = models.CharField(max_length=255, verbose_name="Фамилия заказчика", blank=True, default='')

    #phone_number1 = PhoneNumberField(blank=True, null=True, verbose_name=u"Телефон", region="RU")
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Телефон должен быть в формате: '+79999999999'. ")
    phone_number1 = models.CharField(validators=[phone_regex], max_length=16, blank=True, verbose_name="Телефон")  # validators should be a list
    created = models.DateTimeField(auto_now_add=True, verbose_name=u"Дата поступления заявки")
    checked = models.BooleanField(default=False, verbose_name=u"Статус обработки")

    REQUIRED_FIELDS = ['first_name',  'phone_number1', 'email',]




    class Meta:
        ordering = ('created',)
        verbose_name_plural = 'Заявки на мероприятия'
        verbose_name = 'Заявка на меропритие'
        #verbose_name_plural = 'Формы связи'


class PetitionForm(models.Model):
    email = models.EmailField(max_length=255, verbose_name='Email')
    petition = models.TextField(verbose_name="Обращение", blank=True, default="Задайте нам вопрос и мы Вам обязательно перезвоним")
    first_name = models.CharField(max_length=255, verbose_name="Имя заказчика")
    last_name = models.CharField(max_length=255, verbose_name="Фамилия заказчика", blank=True, default='')

    #phone_number1 = PhoneNumberField(blank=True, null=True, verbose_name=u"Телефон", region="RU")
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Телефон должен быть в формате: '+79999999999'. ")
    phone_number1 = models.CharField(validators=[phone_regex],
                                     max_length=16,
                                     blank=True,
                                     verbose_name="Телефон",
                                     null=False)  # validators should be a list
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата поступления заявки")
    checked = models.BooleanField(default=False, verbose_name="Статус обработки")

    REQUIRED_FIELDS = ['first_name',  'phone_number1', 'email',]


    class Meta:
        ordering = ('created',)
        verbose_name_plural = 'Обращения'
        verbose_name = 'Обращение'
        #verbose_name_plural = 'Формы связи'