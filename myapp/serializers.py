from rest_framework import serializers
from .models import *;
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
 
class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__' 

class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = '__all__'  
class RentPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentPayment
        fields = '__all__'  
class MaintenanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maintenance
        fields = '__all__'  
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'  