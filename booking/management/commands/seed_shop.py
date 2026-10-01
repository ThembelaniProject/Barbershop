from django.core.management.base import BaseCommand
from booking.models import Service, Barber

SERVICES = [
    ("Classic Cut", "Scissor cut, neck clean-up and hot towel finish.", 45, 180),
    ("Skin Fade", "Precision fade with razor-clean finish.", 60, 220),
    ("Beard Sculpt", "Shape, line-up and conditioning treatment.", 30, 140),
    ("Cut & Beard", "Classic cut paired with a full beard sculpt.", 75, 290),
    ("Kids Cut", "A clean, comfortable cut for young gents.", 35, 140),
    ("Executive Package", "Cut, beard, hot towel and styling finish.", 90, 360),
]

BARBERS = [
    ("Lebo M.", "Senior Barber", "Precision fades and classic cuts with a modern edge.", "https://images.unsplash.com/photo-1621605815971-fbc98d665033?auto=format&fit=crop&w=700&q=85"),
    ("Jay K.", "Master Barber", "Known for detailed beard work and relaxed consultations.", "https://images.unsplash.com/photo-1599351431202-1e0f0137899a?auto=format&fit=crop&w=700&q=85"),
    ("Sizwe D.", "Barber", "Clean finishes, kids cuts and sharp everyday styles.", "https://images.unsplash.com/photo-1503951914875-452162b0f3f1?auto=format&fit=crop&w=700&q=85"),
]


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for name, description, duration, price in SERVICES:
            Service.objects.update_or_create(
                name=name,
                defaults={"description": description, "duration_minutes": duration, "price": price, "active": True},
            )
        for name, role, bio, image_url in BARBERS:
            Barber.objects.update_or_create(
                name=name,
                defaults={"role": role, "bio": bio, "image_url": image_url, "active": True},
            )
        self.stdout.write(self.style.SUCCESS("Shop services and barbers seeded with images."))
