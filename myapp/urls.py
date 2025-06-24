from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    manage_rentpayment, manage_maintenance,
    manage_tenant, manage_property, manage_booking,
    get_dashboard_counts,
    TenantRegisterView,  # Add this import
)

urlpatterns = [
    path('rentpayment/', manage_rentpayment),
    path('rentpayment/<int:id>/', manage_rentpayment),
    path('maintenance/', manage_maintenance),
    path('maintenance/<int:id>/', manage_maintenance),
    path('tenant/', manage_tenant),
    path('tenant/<int:id>/', manage_tenant),
    path('property/', manage_property),
    path('property/<int:id>/', manage_property),
    path('booking/', manage_booking),
    path('booking/<int:id>/', manage_booking),

    # Registration endpoint (open, no auth required)
    path('register/', TenantRegisterView.as_view(), name='tenant-register'),

    # JWT Authentication endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),        # Login with JWT
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('dashboard-counts/', get_dashboard_counts),
]
