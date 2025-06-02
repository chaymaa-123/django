from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db.models.functions import TruncMonth
from django.db.models import Count

from .models import Reservation, Voiture,car
from .forms import ReservationForm, VoitureForm, InscriptionForm, ConnexionForm

# --- Pages publiques --- #

def home(request):
    return render(request, 'main.html')

from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Voiture, Reservation

def Contactus_view(request):
    voitures = Voiture.objects.all()

    if request.method == "POST":
        lieu_depart = request.POST.get('pickup_location')
        lieu_retour = request.POST.get('dropoff_location')
        modele_voiture = request.POST.get('modele_voiture')
        datelocation = request.POST.get('datelocation')

        try:
            voiture_obj = Voiture.objects.get(modele=modele_voiture)
        except Voiture.DoesNotExist:
            messages.error(request, "Voiture non trouvée.")
            return redirect('contactus')

        # ✅ Vérifier le stock avant de réserver
        if voiture_obj.stock <= 0:
            messages.error(request, f"La voiture {voiture_obj.modele} est actuellement indisponible.")
            return redirect('contactus')

        # ✅ Créer la réservation si le stock est suffisant
        Reservation.objects.create(
            voiture=voiture_obj,
            lieu_depart=lieu_depart,
            lieu_arrivee=lieu_retour,
            datelocation=datelocation
        )

        messages.success(request, "Réservation enregistrée avec succès.")
        return redirect('contactus')

    return render(request, 'Contactus.html', {'voitures': voitures})


def About(request):
    voitures = car.objects.all()
    return render(request, 'apropos.html', {'cars': voitures})

def VoitureL(request):
    voitures = Voiture.objects.all()
    return render(request, 'VoitureLuxe.html', {'voitures': voitures})

def voitureN(request):
    voitures = Voiture.objects.all()
    return render(request, 'VoitureNrml.html', {'voitures': voitures})

def help(request):
    return render(request, 'help.html')


# --- Compte utilisateur --- #

def compte_view(request):
    if request.method == 'POST':
        if 'btn_inscription' in request.POST:
            form = InscriptionForm(request.POST)
            connexion_form = ConnexionForm()
            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, "Inscription réussie !")
                return redirect('/admin/' if user.is_staff else 'home')
            else:
                messages.error(request, "Erreur lors de l'inscription.")
            show_register = True

        elif 'btn_connexion' in request.POST:
            connexion_form = ConnexionForm(request.POST)
            form = InscriptionForm()
            if connexion_form.is_valid():
                user = authenticate(
                    request,
                    username=connexion_form.cleaned_data['username'],
                    password=connexion_form.cleaned_data['password']
                )
                if user:
                    login(request, user)
                    messages.success(request, "Connexion réussie !")
                    return redirect('/admin/' if user.is_staff else 'home')
                else:
                    messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
            show_register = False
    else:
        form = InscriptionForm()
        connexion_form = ConnexionForm()
        show_register = False

    return render(request, 'compte.html', {
        'form': form,
        'connexion_form': connexion_form,
        'show_register': show_register,
    })


# --- Administration : Gestion des réservations --- #

def gestion_reservations(request):
    reservations = Reservation.objects.all()
    edit_reservation = None

    if 'edit' in request.GET:
        edit_reservation = get_object_or_404(Reservation, id=request.GET['edit'])
    elif 'delete' in request.GET:
        get_object_or_404(Reservation, id=request.GET['delete']).delete()
        return redirect('gestion_reservations')

    if request.method == 'POST':
        reservation_id = request.POST.get('reservation_id')
        if reservation_id:
            instance = get_object_or_404(Reservation, id=reservation_id)
            form = ReservationForm(request.POST, instance=instance)
        else:
            form = ReservationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('gestion_reservations')
    else:
        form = ReservationForm(instance=edit_reservation)

    return render(request, 'admin/gestion_reservations.html', {
        'reservations': reservations,
        'form': form,
        'edit_reservation': edit_reservation,
        'total_reservations': reservations.count(),
    })


# --- Administration : Gestion des voitures --- #

from django.shortcuts import render, redirect, get_object_or_404
from .models import Voiture
from .forms import VoitureForm ,CustomUserForm

def gestion_produits(request):
    voitures = Voiture.objects.all()
    edit_voiture = None

    # Supprimer une voiture
    if 'delete' in request.GET:
        get_object_or_404(Voiture, id=request.GET['delete']).delete()
        return redirect('gestion_produits')

    # Modifier une voiture
    if 'edit' in request.GET:
        edit_voiture = get_object_or_404(Voiture, id=request.GET['edit'])

    # Enregistrer une voiture (ajout ou édition)
    if request.method == 'POST':
        voiture_id = request.POST.get('voiture_id')
        if voiture_id:
            voiture = get_object_or_404(Voiture, id=voiture_id)
            form = VoitureForm(request.POST, instance=voiture)
        else:
            form = VoitureForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('gestion_produits')
    else:
        form = VoitureForm(instance=edit_voiture)

    total_stock = sum(v.stock for v in voitures)
    low_stock_count = sum(1 for v in voitures if v.stock < 5)

    return render(request, 'admin/voiture.html', {
        'voitures': voitures,
        'form': form,
        'edit_voiture': edit_voiture,
        'total_stock': total_stock,
        'low_stock_count': low_stock_count,
    })


def voiture_api(request, id):
    voiture = get_object_or_404(Voiture, id=id)
    data = {
        'id': voiture.id,
        'modele': voiture.modele,
        'prix_de_reservation': float(voiture.prix_de_reservation),
        'type_voiture': voiture.type_voiture,
        'gamme': voiture.typeVoiture,
        'stock': voiture.stock,
    }
    return JsonResponse(data)


# --- Administration : Gestion des comptes --- #

def gestion_comptes(request):
    users = User.objects.all()
    user_to_edit = None

    if 'edit' in request.GET:
        user_to_edit = get_object_or_404(User, pk=request.GET['edit'])

    if 'delete' in request.GET:
        get_object_or_404(User, pk=request.GET['delete']).delete()
        return redirect('gestion_comptes')

    if request.method == 'POST':
        if 'user_id' in request.POST:
            user = get_object_or_404(User, pk=request.POST.get('user_id'))
            form = CustomUserForm(request.POST, instance=user)
        else:
            form = CustomUserForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            if password:
                user.set_password(password)
            user.save()
            return redirect('gestion_comptes')
    else:
        form = CustomUserForm(instance=user_to_edit)

    return render(request, 'admin/gestion_comptes.html', {
        'users': users,
        'form': form,
        'edit_user': user_to_edit,
    })

from django.shortcuts import render
from .models import Voiture, Reservation
from django.db.models import Avg

def admin(request):
    total_voitures = Voiture.objects.count()
    total_reservations = Reservation.objects.count()
    prix_moyen = Voiture.objects.aggregate(moyen=Avg('prix_de_reservation'))['moyen'] or 0

    return render(request, 'admin/dashboard.html', {
        'total_voitures': total_voitures,
        'total_reservations': total_reservations,
        'prix_moyen': round(prix_moyen, 2),
    })

# --- Statistiques --- #

def statistiques_admin(request):
    voitures_by_month = (
        Voiture.objects
        .annotate(month=TruncMonth('date_ajout'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    types_voiture = (
        Voiture.objects
        .values('type_voiture')
        .annotate(total=Count('id'))
    )

    return render(request, 'admin/statistiques.html', {
        'total_users': User.objects.count(),
        'total_voitures': Voiture.objects.count(),
        'total_reservations': Reservation.objects.count(),
        'voitures_by_month': voitures_by_month,
        'types_voiture': types_voiture,
    })
