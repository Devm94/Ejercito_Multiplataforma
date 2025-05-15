from django.urls import path
from multiplataforma import settings
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('inicio_2/', views.inicio_2, name='inicio_2'),
    path('load-municipios/', views.load_municipios, name='load_municipios'),
    path('load-cv/', views.load_cv, name='load_cv'),
    path('cargar_cv/', views.cargar_cv, name='cargar_cv'),
    path('cargar_guia_tel/', views.cargar_guia, name='cargar_guia'),
    path('cv', views.frm_princ_cv , name='cv'),
    path('mapa', views.frm_mapa , name='mapa'),
    path('guia', views.guia_tel , name='guia_tel'),
    path('dashboard', views.dashboard , name='dashboard'),
    path('registrar/', views.registrar_manual, name='registrar_manual'),
    path('actualizar_cv/', views.actualizar_cv, name='actualizar_cv'),
]
