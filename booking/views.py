from urllib.parse import quote
from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.utils import timezone
from .forms import BookingForm
from .models import Service,Barber,Booking
SHOP_NAME="The Gents' Corner Barber Co."
SHOP_ADDRESS="12 Florida Road, Morningside, Durban, KwaZulu-Natal"
def home(request): return render(request,"home.html",{"services":Service.objects.filter(active=True)[:4],"barbers":Barber.objects.filter(active=True)})
def services(request): return render(request,"services.html",{"services":Service.objects.filter(active=True)})
def about(request): return render(request,"about.html",{"barbers":Barber.objects.filter(active=True)})
def contact(request): return render(request,"contact.html")
def terms(request): return render(request,"terms.html")
def book(request):
    form=BookingForm(request.POST or None)
    if request.method=="POST" and form.is_valid():
        b=form.save(); request.session["booking_id"]=b.pk; return redirect("booking_success",booking_id=b.pk)
    return render(request,"booking.html",{"form":form})
def booking_success(request,booking_id):
    b=get_object_or_404(Booking,pk=booking_id)
    if request.session.get("booking_id")!=b.pk: return redirect("book")
    return render(request,"booking_success.html",{"booking":b,"google_url":google_url(b)})
def google_url(b):
    start=timezone.localtime(b.appointment_at).strftime("%Y%m%dT%H%M%S"); end=timezone.localtime(b.end_at).strftime("%Y%m%dT%H%M%S")
    params="&".join([f"action=TEMPLATE",f"text={quote(SHOP_NAME+' — '+b.service.name)}",f"dates={start}/{end}",f"location={quote(SHOP_ADDRESS)}",f"details={quote('Barber: '+b.barber.name+' | Customer: '+b.customer_name)}"])
    return "https://calendar.google.com/calendar/render?"+params
def calendar_ics(request,booking_id):
    b=get_object_or_404(Booking,pk=booking_id); start=timezone.localtime(b.appointment_at).strftime("%Y%m%dT%H%M%S"); end=timezone.localtime(b.end_at).strftime("%Y%m%dT%H%M%S")
    body="BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//Gents Corner//Booking//EN\r\nBEGIN:VEVENT\r\nUID:booking-%s@gentscorner.local\r\nDTSTART:%s\r\nDTEND:%s\r\nSUMMARY:%s\r\nLOCATION:%s\r\nDESCRIPTION:%s\r\nEND:VEVENT\r\nEND:VCALENDAR\r\n"%(b.pk,start,end,b.service.name,SHOP_ADDRESS,"Barber: "+b.barber.name)
    r=HttpResponse(body,content_type="text/calendar"); r["Content-Disposition"]=f'attachment; filename="barber-appointment-{b.pk}.ics"'; return r
