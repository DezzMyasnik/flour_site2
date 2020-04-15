from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import ActivFormSerializers, PetitionFormSerializers
from django.core.mail import send_mail, mail_admins
from django.conf import settings
from rest_framework import generics
from .models import ActivForm
from shop.models import Product
from rest_framework.renderers import TemplateHTMLRenderer
from django.shortcuts import get_object_or_404


def email_client(request):
    email_to = []
    email_to.append(request['email'])  # ActivForm.objects.get(email=request['email'])

    pr = Product.objects.get(id=request['product_id'])
    print(pr)
    msg_html = '<p>Здарвствуйте, {}! </p>' \
               '<p>Вы оставили заявку на покупку билета на {}</p>' \
               '<p>Наши менеджеры свяжутся с Вами по тел {} </p>' \
               '<p>в ближайшее время для уточнения деталей</p> ' \
               '<p>Адмнистрация StudioMyka.(c) тел. +7 (495) 123-37-99 </p>'.format(request['first_name'], pr,
                                                                                    request['phone_number1'])
    template_email_text = ''
    # отправка почты на почту администратора
    msg_html_to_moderator = '<p>Поступила заявка от {} </p>' \
                            '<p> на покупку билета на мероприятие: {} , дата: {}</p>' \
                            '<p>почта клиента: {} </p>' \
                            '<p>телефон клиента: {} </p>'.format(request['first_name'], pr, pr.dateofevent,
                                                                 request['email'], request['phone_number1'])

    mail_admins(' #{}'.format(request['email']), template_email_text, html_message=msg_html_to_moderator,
                fail_silently=False)
    # отправка почты клиету с подтверждением об оставленой заявке
    return send_mail('Заявка на мероприятие', template_email_text, settings.EMAIL_HOST_USER,
                     email_to, html_message=msg_html, fail_silently=False)


def email_client_petition(request):
    email_to = []
    email_to.append(request['email'])
    msg_html = '<p>Здарвствуйте, {}! </p>' \
               '<p>Мы зарегистрировавли Ваше обращение</p>' \
               '<p>Наши менеджеры свяжутся с Вами по тел <b>{}</b></p>' \
               '<p>в ближайшее время для уточнения деталей</p> ' \
               '<p>Адмнистрация StudioMyka.(c) тел. +7 (495) 123-37-99</p> '.format(request['first_name'],
                                                                                    request['phone_number1'])

    template_email_text = ''

    petition = request['petition']

    # отправка почты на почту администратора
    msg_html_to_moderator = '<p>Поступило обращение {} {} </p>' \
                            '<p> Текст обращения: <b>{}</b> </p>' \
                            '<p> почта клиента: {} </p>' \
                            '<p> телефон клиента: {} </p>'.format(request['first_name'], request['last_name'],
                                                                  petition, request['email'],
                                                                  request['phone_number1'])
    mail_admins(' #{}'.format(request['email']),
                template_email_text,
                html_message=msg_html_to_moderator,
                fail_silently=False)

    # отправка почты клиету с подтверждением об оставленой заявке
    return send_mail('Обращение в StudioMyka',
                     template_email_text,
                     settings.EMAIL_HOST_USER,
                     email_to,
                     html_message=msg_html,
                     fail_silently=False)


class ActiveFormApiView(generics.ListCreateAPIView):
    queryset = ''
    serializer_class = ActivFormSerializers
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'sample.html'

    permission_classes = [AllowAny, ]

    def get(self, request):
        active = get_object_or_404(ActivForm)
        serializer = ActivFormSerializers(active)

        return Response({'serializer': serializer, 'form': active})


    def post(self, request, *args, **kwargs):
        email_client(self.request.data)

        return self.create(request, *args, **kwargs)


class PetitionFormApiView(generics.ListCreateAPIView):
    queryset = ''
    serializer_class = PetitionFormSerializers
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        email_client_petition(self.request.data)

        return self.create(request, *args, **kwargs)
