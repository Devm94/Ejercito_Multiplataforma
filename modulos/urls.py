from django.urls import path
from multiplataforma import settings
from . import views
from django.conf.urls.static import static
from .views import cargar_shapefile

urlpatterns = [
    path('', views.inicio_2, name='inicio_2'),
    path('load-municipios/', views.load_municipios, name='load_municipios'),
    path('load-cv/', views.load_cv, name='load_cv'),
    path('cargar_cv/', views.cargar_cv, name='cargar_cv'),
    path('cargar_guia_tel/', views.cargar_contactos, name='cargar_guia'),
    path('cargar-shapefile/', cargar_shapefile, name='cargar_shapefile'),
    path('cv', views.frm_princ_cv , name='cv'),
    path('admin_cv', views.frm_adminxunidad_cv , name='admin_cv'),
    path('mapa', views.frm_mapa , name='mapa'),
    path('guia', views.guia_tel , name='guia_tel'),
    path('guia_cv', views.guia_tel_cv , name='guia_cv'),
    path('rpt_info_gen', views.rpt_info_gen , name='rpt_info_gen'),
    path('rpt_info_situacion', views.rpt_info_situacion , name='rpt_info_situacion'),
    path('registrar/', views.registrar_manual, name='registrar_manual'),
    path('actualizar_cv/', views.actualizar_cv, name='actualizar_cv'),
    path('centro/actualizar_estado/', views.actualizar_estado_cv, name='actualizar_estado'),
    path('centro/detalle/<int:centro_id>/', views.detalle_centro, name='centro_detalle'),
    path('obtener_datos_cv/', views.obtener_datos_cv, name='obtener_datos_cv'),
    path('eliminar_contacto/', views.eliminar_contacto, name='eliminar_contacto'),
    path('mapa1/', views.mapa_municipios, name='mapa_municipios'),
    path('municipios.geojson', views.geojson_municipios, name='geojson_municipios'),
    path('rpt_info_depto/', views.mapa_departamento, name='rpt_info_depto'),
    path('geojson/<str:departamento>/', views.geojson_departamento, name='geojson_departamento'),
    path('centros/<str:id_departamento>/', views.centros_por_departamento, name='centros_por_departamento'),
    path("centros_municipio/<str:cod_municipio>/", views.centros_por_municipio, name="centros_por_municipio"),
    path('centro/<int:centro_id>/personal/', views.obtener_personal_cv, name='obtener_personal_cv'),
    path('centro/agregar_personal/', views.agregar_personal_cv, name='agregar_personal_cv'),
    path('centro/eliminar_personal/<int:id>/', views.eliminar_personal, name='eliminar_personal'),
    path('centro/<int:centro_id>/foto/', views.obtener_foto_cv),
    path('centro/guardar_foto/', views.guardar_foto_cv),
    path('centro/guardar_ubicacion/', views.guardar_ubicacion_cv, name='guardar_ubicacion_cv'),
]
