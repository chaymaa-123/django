from django.contrib import admin
from .models import Voiture, Reservation, car

admin.site.register(Voiture)
admin.site.register(Reservation)
admin.site.register(car)
