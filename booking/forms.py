from django import forms
from django.utils import timezone
from .models import Booking,Service,Barber
class BookingForm(forms.ModelForm):
    class Meta:
        model=Booking
        fields=["service","barber","appointment_at","customer_name","customer_email","customer_phone","notes"]
        widgets={"appointment_at":forms.DateTimeInput(attrs={"type":"datetime-local"}),"customer_name":forms.TextInput(attrs={"placeholder":"Your full name"}),"customer_email":forms.EmailInput(attrs={"placeholder":"you@example.com"}),"customer_phone":forms.TextInput(attrs={"placeholder":"+27 82 000 0000"}),"notes":forms.Textarea(attrs={"rows":3,"placeholder":"Anything we should know?"})}
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["service"].queryset=Service.objects.filter(active=True)
        self.fields["barber"].queryset=Barber.objects.filter(active=True)
    def clean_appointment_at(self):
        value=self.cleaned_data["appointment_at"]
        if timezone.is_naive(value): value=timezone.make_aware(value)
        if value<=timezone.now(): raise forms.ValidationError("Please choose a future appointment.")
        if value.weekday()==6 or value.hour<9 or value.hour>=18: raise forms.ValidationError("Choose Monday–Saturday, 09:00–18:00.")
        barber=self.cleaned_data.get("barber")
        if barber and Booking.objects.filter(barber=barber,appointment_at=value,status="confirmed").exists(): raise forms.ValidationError("That time is already booked with this barber.")
        return value
