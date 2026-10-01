from django.core.management.base import BaseCommand
from booking.models import Service,Barber
SERVICES=[("Classic Cut","Scissor cut, neck clean-up and hot towel finish.",45,180),("Skin Fade","Precision fade with razor-clean finish.",60,220),("Beard Sculpt","Shape, line-up and conditioning treatment.",30,140),("Cut & Beard","Classic cut paired with a full beard sculpt.",75,290),("Kids Cut","A clean, comfortable cut for young gents.",35,140),("Executive Package","Cut, beard, hot towel and styling finish.",90,360)]
BARBERS=[("Lebo M.","Senior Barber","Precision fades and classic cuts with a modern edge."),("Jay K.","Master Barber","Known for detailed beard work and relaxed consultations."),("Sizwe D.","Barber","Clean finishes, kids cuts and sharp everyday styles.")]
class Command(BaseCommand):
    def handle(self,*args,**kwargs):
        for n,d,dur,p in SERVICES: Service.objects.get_or_create(name=n,defaults={"description":d,"duration_minutes":dur,"price":p})
        for n,r,b in BARBERS: Barber.objects.get_or_create(name=n,defaults={"role":r,"bio":b})
        self.stdout.write(self.style.SUCCESS("Shop data seeded."))
