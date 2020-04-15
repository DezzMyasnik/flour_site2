from rest_framework.serializers import (
    ModelSerializer,
)

from rest_framework_recaptcha.fields import ReCaptchaField
from .models import ActivForm, PetitionForm


class ActivFormSerializers(ModelSerializer):
    recaptcha = ReCaptchaField()
    class Meta:
        model = ActivForm

        fields = ('id', 'first_name', 'last_name', 'email', 'phone_number1', 'product_id', 'recaptcha',)


    depth = 3


class PetitionFormSerializers(ModelSerializer):
    recaptcha = ReCaptchaField()
    class Meta:
        model = PetitionForm
        fields = ('id', 'first_name', 'last_name', 'email', 'phone_number1', 'petition', 'recaptcha',)

