from django.conf.urls import url, include
from .serializers import ActivFormSerializers
from .views import ActiveFormApiView, PetitionFormApiView

urlpatterns = [
    url(r'^formact/', ActiveFormApiView.as_view()),
    url(r'^petition/', PetitionFormApiView.as_view())
]
