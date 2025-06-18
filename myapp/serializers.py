from rest_framework import serializers
from .models import *;
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Serializer for User model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'  # Include all fields (userID, username, password, role)

# Serializer for Property model
class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'  # Include all fields (PropertyID, Address, Type, OwnerID)

# Serializer for Tenant model
class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = '__all__'  # Include all fields (TenantID, Name, ContactInfo, LeaseDetails)

# Serializer for RentPayment model
class RentPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentPayment
        fields = '__all__'  # Include all fields (PaymentID, TenantID, Amount, Date, Status)

# Serializer for Maintenance model
class MaintenanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maintenance
        fields = '__all__'  # Include all fields (MaintID, TenantID, PropertyID, Description, Status)

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'  