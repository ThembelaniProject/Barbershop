from django.contrib import admin
from .models import Barber,Service,Booking
@admin.register(Barber)
class BarberAdmin(admin.ModelAdmin): list_display=("name","role","active"); list_filter=("active",)
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin): list_display=("name","price","duration_minutes","active"); list_filter=("active",)
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin): list_display=("customer_name","service","barber","appointment_at","status"); list_filter=("status","barber"); search_fields=("customer_name","customer_email","customer_phone")
