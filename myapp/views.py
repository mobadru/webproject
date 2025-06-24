from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import Tenant, Property, Booking, RentPayment, Maintenance
from .serializers import (
    TenantSerializer,
    PropertySerializer,
    BookingSerializer,
    RentPaymentSerializer,
    MaintenanceSerializer,
)

# Generic API with user filtering and automatic tenant assignment
def generic_api(model_class, serializer_class, user_filter_field=None):
    @api_view(['GET', 'POST', 'PUT', 'DELETE'])
    @permission_classes([IsAuthenticated])
    def api(request, id=None):
        filter_kwargs = {}

        # For tenant filtering, get tenant instance from logged in user
        if user_filter_field == 'tenant':
            try:
                tenant = Tenant.objects.get(user=request.user)
                filter_kwargs['tenant'] = tenant
            except Tenant.DoesNotExist:
                return Response({'message': 'Tenant profile not found for user'}, status=404)

        if request.method == 'GET':
            if id:
                try:
                    if user_filter_field:
                        instance = model_class.objects.get(id=id, **filter_kwargs)
                    else:
                        instance = model_class.objects.get(id=id)
                    serializer = serializer_class(instance)
                    return Response(serializer.data)
                except model_class.DoesNotExist:
                    return Response({'message': 'Object not found'}, status=404)
            else:
                if user_filter_field:
                    instances = model_class.objects.filter(**filter_kwargs)
                else:
                    instances = model_class.objects.all()
                serializer = serializer_class(instances, many=True)
                return Response(serializer.data)

        elif request.method == 'POST':
            serializer = serializer_class(data=request.data)
            if serializer.is_valid():
                if user_filter_field == 'tenant':
                    # Save with tenant from user, ignoring tenant in request.data
                    serializer.save(tenant=tenant)
                elif user_filter_field:
                    serializer.save(**{user_filter_field: request.user})
                else:
                    serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)

        elif request.method == 'PUT':
            if not id:
                return Response({'message': 'ID is required for update'}, status=400)
            try:
                if user_filter_field:
                    instance = model_class.objects.get(id=id, **filter_kwargs)
                else:
                    instance = model_class.objects.get(id=id)
                serializer = serializer_class(instance, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=400)
            except model_class.DoesNotExist:
                return Response({'message': 'Object not found'}, status=404)

        elif request.method == 'DELETE':
            if not id:
                return Response({'message': 'ID is required for deletion'}, status=400)
            try:
                if user_filter_field:
                    instance = model_class.objects.get(id=id, **filter_kwargs)
                else:
                    instance = model_class.objects.get(id=id)
                instance.delete()
                return Response({'message': 'Deleted successfully'}, status=204)
            except model_class.DoesNotExist:
                return Response({'message': 'Object not found'}, status=404)

        return Response({'message': 'Invalid method'}, status=405)

    return api


# Tenant registration - creates User and Tenant profiles
class TenantRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')
        contact_info = data.get('contact_info')

        if not all([username, email, password, name, contact_info]):
            return Response({'message': 'All fields are required'}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({'message': 'Username already taken'}, status=400)
        if User.objects.filter(email=email).exists():
            return Response({'message': 'Email already registered'}, status=400)

        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password)
        )

        tenant = Tenant.objects.create(
            user=user,
            name=name,
            email=email,
            contact_info=contact_info
        )

        serializer = TenantSerializer(tenant)
        return Response(serializer.data, status=201)


# Login view to get JWT tokens
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


# Example dashboard counts for tenant or admin
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_dashboard_counts(request):
    tenant = getattr(request.user, 'tenant_profile', None)

    if tenant:
        counts = {
            "bookings": Booking.objects.filter(tenant=tenant).count(),
            "payments": RentPayment.objects.filter(tenant=tenant).count(),
            "maintenance": Maintenance.objects.filter(tenant=tenant).count(),
        }
    else:
        counts = {
            "tenants": Tenant.objects.count(),
            "properties": Property.objects.count(),
            "bookings": Booking.objects.count(),
            "payments": RentPayment.objects.count(),
            "maintenance": Maintenance.objects.count(),
        }

    return Response(counts)


# Generic APIs with tenant filtering where relevant
manage_rentpayment = generic_api(RentPayment, RentPaymentSerializer, user_filter_field='tenant')
manage_maintenance = generic_api(Maintenance, MaintenanceSerializer, user_filter_field='tenant')
manage_tenant = generic_api(Tenant, TenantSerializer, user_filter_field='user')
manage_property = generic_api(Property, PropertySerializer)  # No user filter for properties (admin or public)
manage_booking = generic_api(Booking, BookingSerializer, user_filter_field='tenant')
