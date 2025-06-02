from datetime import timedelta
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

# Fonction à utiliser pour default
def default_date_fin():
    return timezone.localdate() + timedelta(days=1)

class Voiture(models.Model):
    TYPE_CHOICES = [
        ('LUXE', 'Luxe'),
        ('NORMALE', 'Normale'),
    ]

    TYPE_CHOICES_GAMME = [
        ('Gamme_Familiale', 'Gamme Familiale'),
        ('Gamme_SUV', 'Gamme SUV'),
        ('Gamme_Citadines', 'Gamme Citadines'),
        ('prestige', 'prestige'),
        ('SUVs', 'SUVs'),
        ('Berlines_Limousines', 'Berlines Limousines')
    ]

    modele = models.CharField(max_length=100)
    image_filename = models.TextField() 
    typeVoiture = models.CharField(max_length=10, choices=TYPE_CHOICES, default='NORMALE')
    stock = models.IntegerField(default=5)
    prix_de_reservation = models.DecimalField(max_digits=10, decimal_places=2)
    type_voiture = models.CharField(max_length=20, choices=TYPE_CHOICES_GAMME, default='Gamme_Familiale')
    position = models.DecimalField(max_digits=10, decimal_places=2 ,default=5)

    def __str__(self):
        return f"{self.modele} ({self.get_typeVoiture_display()})"

class Reservation(models.Model):
    lieu_depart = models.CharField(max_length=100)
    lieu_arrivee = models.CharField(max_length=100)
    datelocation = models.CharField(max_length=100)
    voiture = models.ForeignKey(Voiture, on_delete=models.CASCADE)

    def __str__(self):
        return f"Réservation de {self.voiture.modele} ."

class car(models.Model):
    voiture = models.CharField(max_length=100)  
    image_filename = models.TextField()
    type = models.IntegerField(default=0)
    position = models.IntegerField(default=0)

    def __str__(self):
        return self.voiture

from django.db import models








