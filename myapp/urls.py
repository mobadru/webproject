from django.urls import path
from .views import (
    manage_rentpayment, manage_maintenance, manage_user,
    manage_tenant, manage_property, manage_booking, LoginView
)

urlpatterns = [
    path('rentpayment/', manage_rentpayment),
    path('rentpayment/<int:id>/', manage_rentpayment),
    path('maintenance/', manage_maintenance),
    path('maintenance/<int:id>/', manage_maintenance),
    path('user/', manage_user),
    path('user/<int:id>/', manage_user),
    path('tenant/', manage_tenant),
    path('tenant/<int:id>/', manage_tenant),
    path('property/', manage_property),
    path('property/<int:id>/', manage_property),
    path('booking/', manage_booking),
    path('booking/<int:id>/', manage_booking),
    path('login/', LoginView.as_view(), name='login'),
]
