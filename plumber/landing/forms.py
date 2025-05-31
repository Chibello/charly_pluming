from django import forms
from .models import ServiceBooking

class ServiceBookingForm(forms.ModelForm):
    class Meta:
        model = ServiceBooking
        fields = ['name', 'phone_number', 'email', 'service_type', 'preferred_date', 'message']
        widgets = {
            'preferred_date': forms.DateInput(attrs={'type': 'date'}),
        }
