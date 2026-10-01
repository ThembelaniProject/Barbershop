from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models


class Barber(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=120, default="Master Barber")
    bio = models.TextField()
    image_url = models.URLField(blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField()
    duration_minutes = models.PositiveIntegerField(default=45)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Booking(models.Model):
    STATUS = [("confirmed", "Confirmed"), ("cancelled", "Cancelled")]
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    barber = models.ForeignKey(Barber, on_delete=models.PROTECT)
    customer_name = models.CharField(max_length=120)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=40)
    appointment_at = models.DateTimeField()
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default="confirmed")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["appointment_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["barber", "appointment_at"],
                name="unique_barber_slot",
            )
        ]

    def clean(self):
        errors = {}

        # Model validation can run even when the form has missing/invalid
        # fields, so never call weekday() on a missing appointment.
        if self.appointment_at is None:
            errors["appointment_at"] = "Please choose an appointment date and time."
        else:
            if self.appointment_at.weekday() == 6:
                errors["appointment_at"] = "The shop is closed on Sundays."
            elif self.appointment_at.hour < 9 or self.appointment_at.hour >= 18:
                errors["appointment_at"] = "Appointments are between 09:00 and 18:00."

        if self.service is None:
            errors["service"] = "Please choose a service."

        if self.barber is None:
            errors["barber"] = "Please choose a barber."

        if errors:
            raise ValidationError(errors)

    @property
    def end_at(self):
        if self.appointment_at is None or self.service is None:
            return self.appointment_at
        return self.appointment_at + timedelta(minutes=self.service.duration_minutes)

    def __str__(self):
        if self.appointment_at is None:
            return f"{self.customer_name} - Unscheduled appointment"
        return f"{self.customer_name} - {self.appointment_at:%Y-%m-%d %H:%M}"
