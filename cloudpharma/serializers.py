from rest_framework import serializers
from .models import Medcine, Choice

class ConsumptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['choice']

class MedcineSerializer(serializers.ModelSerializer):
    consumption = ConsumptionSerializer(read_only=True, many=True)
    class Meta:
        model = Medcine
        fields = ['id', 'name', 'consumption', 'amount_consumed', 'initial_amount', 'actual_amount', 'purchase_date', 'end_date', 'owner']