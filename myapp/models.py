from django.db import models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
class User(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.username

class Property(models.Model):
    ROOM_STATUS_CHOICES = [
        ('Empty', 'Empty'),
        ('Booked', 'Booked'),
    ]
    room_no = models.CharField(max_length=50, default="Room 1")  # Room number
    status = models.CharField(max_length=10, choices=ROOM_STATUS_CHOICES, default='Empty')  # Status of the room
    type = models.CharField(max_length=100)  # Type of property
    price = models.DecimalField(max_digits=10, decimal_places=2, default=100000)  # Price of the property with default value 100000

    def __str__(self):
        return f"Room {self.room_no} ({self.type}) - {self.status}"

class Tenant(models.Model):
    name = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)
    username = models.CharField(max_length=255,default='Tenant')
    password = models.CharField(max_length=255, default='123')  # Provide a default value

    def __str__(self):
        return self.name

class Booking(models.Model):
    BOOKING_CHOICES = [
        ('Pending', 'Pending'),
        ('Success', 'Success'),
    ]
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="bookings")
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="bookings", default=1)  # Link to Tenant model
    status = models.CharField(max_length=20, default="Pending")
    start_date = models.DateField(default="2025-01-01")  # When the booking starts
    end_date = models.DateField(default="2025-12-1")  # When the booking ends
    price = models.DecimalField(max_digits=10, decimal_places=2, default=1000.00)  # Price of the booking
    status = models.CharField(max_length=10, choices=BOOKING_CHOICES, default='Pending')  # Status of the room

    def __str__(self):
        return (
            f"Booking for Room {self.property.room_no} by {self.tenant.name} - "
            f"{self.status}, Price: {self.price}, "
            f"From {self.start_date} to {self.end_date}"
        )

class RentPayment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Overdue', 'Overdue'),
    ]
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='payments')
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='payments', null=True, blank=True)  # Link to Booking model
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