from urllib.parse import quote

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import BookingForm
from .models import Barber, Booking, Service

SHOP_NAME = "The Gents' Corner Barber Co."
SHOP_ADDRESS = "12 Florida Road, Morningside, Durban, KwaZulu-Natal"


def home(request):
    return render(request, "home.html", {
        "services": Service.objects.filter(active=True)[:4],
        "barbers": Barber.objects.filter(active=True),
    })


def services(request):
    return render(request, "services.html", {"services": Service.objects.filter(active=True)})


def barbers(request):
    return render(request, "barbers.html", {"barbers": Barber.objects.filter(active=True)})


def about(request):
    return render(request, "about.html", {"barbers": Barber.objects.filter(active=True)})


def contact(request):
    return render(request, "contact.html")


def terms(request):
    return render(request, "terms.html")


def book(request):
    form = BookingForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        booking = form.save()
        request.session["booking_id"] = booking.pk
        return redirect("booking_success", booking_id=booking.pk)
    return render(request, "booking.html", {"form": form})


def booking_success(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    if request.session.get("booking_id") != booking.pk:
        return redirect("book")
    return render(request, "booking_success.html", {
        "booking": booking,
        "google_url": google_url(booking),
    })


def google_url(booking):
    start = timezone.localtime(booking.appointment_at).strftime("%Y%m%dT%H%M%S")
    end = timezone.localtime(booking.end_at).strftime("%Y%m%dT%H%M%S")
    params = "&".join([
        "action=TEMPLATE",
        f"text={quote(SHOP_NAME + ' — ' + booking.service.name)}",
        f"dates={start}/{end}",
        f"location={quote(SHOP_ADDRESS)}",
        f"details={quote('Barber: ' + booking.barber.name + ' | Customer: ' + booking.customer_name)}",
    ])
    return "https://calendar.google.com/calendar/render?" + params


def calendar_ics(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    start = timezone.localtime(booking.appointment_at).strftime("%Y%m%dT%H%M%S")
    end = timezone.localtime(booking.end_at).strftime("%Y%m%dT%H%M%S")
    body = (
        "BEGIN:VCALENDAR\\r\\nVERSION:2.0\\r\\nPRODID:-//Gents Corner//Booking//EN\\r\\n"
        "BEGIN:VEVENT\\r\\nUID:booking-%s@gentscorner.local\\r\\nDTSTART:%s\\r\\nDTEND:%s\\r\\n"
        "SUMMARY:%s\\r\\nLOCATION:%s\\r\\nDESCRIPTION:%s\\r\\nEND:VEVENT\\r\\nEND:VCALENDAR\\r\\n"
        % (booking.pk, start, end, booking.service.name, SHOP_ADDRESS, "Barber: " + booking.barber.name)
    )
    response = HttpResponse(body, content_type="text/calendar")
    response["Content-Disposition"] = f'attachment; filename="barber-appointment-{booking.pk}.ics"'
    return response
