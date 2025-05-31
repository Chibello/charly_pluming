from django.db import models

# Create your models here
from django.contrib.auth.models import User

class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, null=True)
    email = models.EmailField(max_length=255)

    def __str__(self):
        return self.user.username
    
###########################################################################################

class ServiceBooking(models.Model):
    SERVICE_CHOICES = [
        ('leak_repair', 'Leak Repair'),
        ('pipe_installation', 'Pipe Installation'),
        ('drain_cleaning', 'Drain Cleaning'),
        ('emergency_plumbing', 'Emergency Plumbing'),
    ]
    
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    service_type = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    preferred_date = models.DateField()
    message = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} - {self.service_type}"
