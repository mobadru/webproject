from django.contrib import admin
from .models import User, Property, Tenant, RentPayment, Maintenance
from .models import Booking
admin.site.register(User)
admin.site.register(Property)
admin.site.register(Tenant)
admin.site.register(RentPayment)
admin.site.register(Maintenance)
admin.site.register(Booking)
