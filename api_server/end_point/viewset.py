from .serializers import CurrencySerializer
from .models import Currency_value
from rest_framework import viewsets


class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency_value.objects.all()
    serializer_class = CurrencySerializer