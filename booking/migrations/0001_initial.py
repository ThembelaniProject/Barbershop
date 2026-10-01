from django.db import migrations,models
import django.db.models.deletion
class Migration(migrations.Migration):
    initial=True
    dependencies=[]
    operations=[
        migrations.CreateModel(name="Barber",fields=[("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),("name",models.CharField(max_length=100)),("role",models.CharField(default="Master Barber",max_length=120)),("bio",models.TextField()),("image_url",models.URLField(blank=True)),("active",models.BooleanField(default=True))]),
        migrations.CreateModel(name="Service",fields=[("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),("name",models.CharField(max_length=120)),("description",models.TextField()),("duration_minutes",models.PositiveIntegerField(default=45)),("price",models.DecimalField(decimal_places=2,max_digits=8)),("active",models.BooleanField(default=True))]),
        migrations.CreateModel(name="Booking",fields=[("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),("customer_name",models.CharField(max_length=120)),("customer_email",models.EmailField(max_length=254)),("customer_phone",models.CharField(max_length=40)),("appointment_at",models.DateTimeField()),("notes",models.TextField(blank=True)),("status",models.CharField(choices=[("confirmed","Confirmed"),("cancelled","Cancelled")],default="confirmed",max_length=20)),("created_at",models.DateTimeField(auto_now_add=True)),("barber",models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,to="booking.barber")),("service",models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,to="booking.service"))]),
        migrations.AddConstraint(model_name="booking",constraint=models.UniqueConstraint(fields=("barber","appointment_at"),name="unique_barber_slot"))
    ]
