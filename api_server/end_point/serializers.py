from rest_framework_json_api import serializers
from .models import Currency_value


class CurrencySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Currency_value
        fields = ('name', 'rating', 'restaurant')