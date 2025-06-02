from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Reservation, Voiture

print("✅ Signals chargés !")

@receiver(post_save, sender=Reservation)
def diminuer_stock(sender, instance, created, **kwargs):
    if created:
        print("🟢 Réservation créée : stock diminué")
        voiture = instance.voiture
        if voiture.stock > 0:
            voiture.stock -= 1
            voiture.save()
        else:
            raise ValueError("Stock épuisé")

@receiver(post_delete, sender=Reservation)
def augmenter_stock(sender, instance, **kwargs):
    print("🟠 Réservation supprimée : stock augmenté")
    voiture = instance.voiture
    voiture.stock += 1
    voiture.save()
