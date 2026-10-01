from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Barber, Booking, Service


class BookingFlowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.service = Service.objects.create(
            name="Test Cut",
            description="Test service",
            duration_minutes=45,
            price="180.00",
            active=True,
        )
        cls.barber = Barber.objects.create(
            name="Test Barber",
            role="Master Barber",
            bio="Test barber profile",
            active=True,
        )

    def future_weekday(self):
        value = timezone.localtime(timezone.now()) + timedelta(days=3)
        while value.weekday() == 6:
            value += timedelta(days=1)
        return value.replace(hour=10, minute=0, second=0, microsecond=0)

    def test_public_pages_load(self):
        for name in ["home", "services", "barbers", "about", "contact", "book", "terms"]:
            response = self.client.get(reverse(name))
            self.assertEqual(response.status_code, 200, name)

    def test_booking_creates_confirmation_and_calendar_links(self):
        appointment = self.future_weekday()
        response = self.client.post(reverse("book"), {
            "service": self.service.pk,
            "barber": self.barber.pk,
            "appointment_at": appointment.strftime("%Y-%m-%dT%H:%M"),
            "customer_name": "Test Guest",
            "customer_email": "guest@example.com",
            "customer_phone": "+27820000000",
            "notes": "Test appointment",
        })

        self.assertRedirects(response, reverse("booking_success", kwargs={"booking_id": 1}))
        booking = Booking.objects.get(pk=1)

        confirmation = self.client.get(
            reverse("booking_success", kwargs={"booking_id": booking.pk})
        )
        self.assertContains(confirmation, "Add to Google Calendar")
        self.assertContains(confirmation, "Add to Apple Calendar")

        google = confirmation.context["google_url"]
        self.assertIn("calendar.google.com", google)
        self.assertIn("dates=", google)
        self.assertIn("ctz=Africa%2FJohannesburg", google)

        ics = self.client.get(
            reverse("calendar_ics", kwargs={"booking_id": booking.pk})
        )
        self.assertEqual(ics.status_code, 200)
        self.assertEqual(ics["Content-Type"], "text/calendar; charset=utf-8")
        self.assertIn("DTSTART;TZID=Africa/Johannesburg:", ics.content.decode())
        self.assertIn("DTEND;TZID=Africa/Johannesburg:", ics.content.decode())
        self.assertIn("Test Cut", ics.content.decode())
        self.assertIn("12 Florida Road", ics.content.decode())

    def test_sunday_is_rejected(self):
        appointment = self.future_weekday()
        while appointment.weekday() != 6:
            appointment += timedelta(days=1)

        response = self.client.post(reverse("book"), {
            "service": self.service.pk,
            "barber": self.barber.pk,
            "appointment_at": appointment.strftime("%Y-%m-%dT%H:%M"),
            "customer_name": "Test Guest",
            "customer_email": "guest@example.com",
            "customer_phone": "+27820000000",
            "notes": "",
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "closed on Sundays")

    def test_service_cannot_finish_after_closing(self):
        appointment = self.future_weekday().replace(hour=17, minute=30)
        response = self.client.post(reverse("book"), {
            "service": self.service.pk,
            "barber": self.barber.pk,
            "appointment_at": appointment.strftime("%Y-%m-%dT%H:%M"),
            "customer_name": "Test Guest",
            "customer_email": "guest@example.com",
            "customer_phone": "+27820000000",
            "notes": "",
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ends after 18:00")
