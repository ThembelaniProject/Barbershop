from datetime import timedelta

from django import forms
from django.utils import timezone

from .models import Barber, Booking, Service


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            "service", "barber", "appointment_at", "customer_name",
            "customer_email", "customer_phone", "notes",
        ]
        widgets = {
            "appointment_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "customer_name": forms.TextInput(attrs={"placeholder": "Your full name", "autocomplete": "name"}),
            "customer_email": forms.EmailInput(attrs={"placeholder": "you@example.com", "autocomplete": "email"}),
            "customer_phone": forms.TextInput(attrs={"placeholder": "+27 82 000 0000", "autocomplete": "tel"}),
            "notes": forms.Textarea(attrs={"rows": 3, "placeholder": "Anything we should know?"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["service"].queryset = Service.objects.filter(active=True)
        self.fields["barber"].queryset = Barber.objects.filter(active=True)
        self.fields["service"].empty_label = "Choose a service"
        self.fields["barber"].empty_label = "Choose your barber"

    def clean_appointment_at(self):
        value = self.cleaned_data["appointment_at"]
        if timezone.is_naive(value):
            value = timezone.make_aware(value)
        if value <= timezone.now():
            raise forms.ValidationError("Please choose a future appointment.")
        if value.weekday() == 6 or value.hour < 9 or value.hour >= 18:
            raise forms.ValidationError("Choose Monday–Saturday, 09:00–18:00.")

        barber = self.cleaned_data.get("barber")
        service = self.cleaned_data.get("service")
        if barber and service:
            requested_start = value
            requested_end = value + timedelta(minutes=service.duration_minutes)
            existing = Booking.objects.filter(
                barber=barber,
                status="confirmed",
                appointment_at__lt=requested_end,
            ).exclude(pk=self.instance.pk)
            for booking in existing:
                if booking.end_at > requested_start:
                    raise forms.ValidationError(
                        f"{barber.name} is already booked around that time. Please choose another time."
                    )
        return value
