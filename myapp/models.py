from django.db import models
from django.contrib.auth.models import User 
import datetime

class Property(models.Model):
    ROOM_STATUS_CHOICES = [
        ('Empty', 'Empty'),
        ('Booked', 'Booked'),
    ]
    room_no = models.CharField(max_length=50, default="Room 1")
    status = models.CharField(max_length=10, choices=ROOM_STATUS_CHOICES, default='Empty')
    type = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=100000)

    def __str__(self):
        return f"Room {self.room_no} ({self.type}) - {self.status}"

class Tenant(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='tenant_profile',
        null=True, blank=True )
    name = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name

class Booking(models.Model):
    BOOKING_CHOICES = [
        ('Pending', 'Pending'),
        ('Success', 'Success'),
    ]
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="bookings")
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="bookings", null=True, blank=True)
    start_date = models.DateField(default=datetime.date(2025, 1, 1))
    end_date = models.DateField(default=datetime.date(2025, 12, 1))
    price = models.DecimalField(max_digits=10, decimal_places=2, default=1000.00)
    status = models.CharField(max_length=10, choices=BOOKING_CHOICES, default='Pending')

    def __str__(self):
        return f"Booking for {self.tenant.name if self.tenant else 'Unknown Tenant'} in {self.property.room_no} ({self.status})"

class RentPayment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Overdue', 'Overdue'),
    ]
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='payments')
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='payments', null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)

    def __str__(self):
        return f"Payment {self.id} - {self.amount} by {self.tenant.name}"

class Maintenance(models.Model):
    STATUS_CHOICES = [
        ('Requested', 'Requested'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='maintenance_requests')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='maintenance_requests')
    description = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)

    def __str__(self):
        return f"Maintenance {self.id}"
