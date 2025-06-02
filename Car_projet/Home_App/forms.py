from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Voiture
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['lieu_depart', 'lieu_arrivee', 'datelocation', 'voiture']
        widgets = {
            'lieu_depart': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-black-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-700',
                'placeholder': 'Lieu de départ'
            }),
            'lieu_arrivee': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-black-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-700',
                'placeholder': 'Lieu de retour'   
            }),
            'datelocation': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-black-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-700',
                'type': 'date',         
                'placeholder': 'JJ/MM/AAAA'
            }),
            'voiture': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-black-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-700',
            }),
        }


class VoitureForm(forms.ModelForm):
    class Meta:
        model = Voiture
        fields = ['modele', 'prix_de_reservation', 'type_voiture', 'typeVoiture', 'stock']

        widgets = {
            'modele': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-black-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-700',
                'placeholder': 'Modèle de la voiture'
            }),
            'prix_de_reservation': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-black-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-700',
                'placeholder': 'Prix de réservation'
            }),
            'type_voiture': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-black-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-700',
                'placeholder': 'Type de voiture (ex: SUV, Berline, etc.)'   
            }),
            'typeVoiture': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-black-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-700',
                'placeholder': 'Type de voiture'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-black-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-700',
            }),
        }
from django import forms
from .models import User  # Ton propre modèle

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class InscriptionForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_staff = False  # <-- ICI tu forces à False à l'inscription publique
        if commit:
            user.save()
        return user

class ConnexionForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
from django import forms
from django.contrib.auth.models import User

class CustomUserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(),
        label="Mot de passe",
        required=False
    )
    
    is_staff = forms.BooleanField(
        label="Est admin",
        required=False,
        initial=True
    )

    is_superuser = forms.BooleanField(
        label="Est superutilisateur",
        required=False,
        initial=True
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'is_staff', 'is_superuser']
        labels = {
            'username': 'Nom d’utilisateur',
            'email': 'Adresse e-mail',
        }
