from django.urls import path
from . import views
urlpatterns=[path("",views.home,name="home"),path("services/",views.services,name="services"),path("about/",views.about,name="about"),path("contact/",views.contact,name="contact"),path("booking/",views.book,name="book"),path("booking/success/<int:booking_id>/",views.booking_success,name="booking_success"),path("booking/<int:booking_id>/calendar.ics",views.calendar_ics,name="calendar_ics"),path("terms/",views.terms,name="terms")]
