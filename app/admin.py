from django.contrib import admin

# Register your models here.
from app.models import Doctor, Availability

admin.site.register(Doctor)
admin.site.register(Availability)