from django.db import models
from django.core.validators import RegexValidator
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, pre_delete
from django.urls import reverse
from django.core.mail import send_mail
import os

from .utils import code_generator


User = settings.AUTH_USER_MODEL


class Gender(models.Model):
    sex = models.CharField(max_length=12)

    def __str__(self):
        return self.sex


class Accounts(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(default='default.png', blank=True, null=True)
    region = models.CharField(max_length=255, blank=True, null=True)
    address1 = models.CharField(max_length=255, blank=True, null=True)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    phone_number1 = models.IntegerField(blank=True, null=True)
    phone_number2 = models.IntegerField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    activation_key = models.CharField(max_length=120, blank=True, null=True)
    activated = models.BooleanField(default=False)
    block_review = models.BooleanField(default=False)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_anonymous = models.BooleanField(default=False)
    is_authenticated = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number1']
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('accounts:update', kwargs={'pk': self.id})

    def send_activation_email(self):
        if not self.activated:
            self.activation_key = code_generator()
            self.save()
            path = reverse('accounts:activate', kwargs={'code': self.activation_key})
            subject = 'Activate Account'
            from_email = settings.DEFAULT_FROM_EMAIL
            message = 'Activate your acounts here: {}'.format(path)
            recipient_list = [self.user.email]
            html_message = '<p>Activate your acounts here: {}</p>'.format(path)
            print(html_message)
            sent_mail = send_mail(
                subject,
                message,
                from_email,
                recipient_list,
                fail_silently=False,
                html_message=html_message)
            return sent_mail


def post_save_user_receiver(sender, instance, created, *args, **kwargs):
    if created:
        profile, is_created = Accounts.objects.get_or_create(
            user=instance,
            first_name=instance.first_name,
            last_name=instance.last_name,
            username=instance.username,
            email=instance.email,
        )


def pre_delete_account_img(sender, instance, *args, **kwargs):
    if instance.image:
        if instance.image == 'default.png':
            pass
        else:
            if os.path.isfile(instance.image.path):
                os.remove(instance.image.path)


pre_delete.connect(pre_delete_account_img, sender=Accounts)
post_save.connect(post_save_user_receiver, sender=User)