"""
URL configuration for Car_projet project.

The urlpatterns list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from Home_App import views as hv
urlpatterns = [
    path('admin/', hv.admin,name='admin'),
    path('home/',hv.home,name='home'),
    path('Contactus/', hv.Contactus_view, name='contactus'),
    path('Aboutus/', hv.About),
    path('VoitureLuxe/',hv.VoitureL),
  
    path('VoitureNrml/',hv.voitureN),
    path('help/',hv.help),    
    path('', hv.compte_view, name='compte'),
   path('reservations/', hv.gestion_reservations, name='gestion_reservations'),

 path('admin/voitures/', hv.gestion_produits, name='gestion_produits'),
 path('admin/reservations/', hv.gestion_reservations, name='gestion_reservations'),
   path('admin/gestion-comptes/', hv.gestion_comptes, name='gestion_comptes'),
   path('admin/statistiques/', hv.statistiques_admin, name='statistiques_admin')


]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)