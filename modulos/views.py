from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
import pandas as pd
from .models import *

list_deptos = depto.objects.all()
list_munic = munic.objects.all()

def inicio(request):
    return render(request, 'index.html')

def inicio_2(request):
    return render(request, 'core/base.html')

def dashboard(request):
    return render(request, 'cv/form_dashboard.html')


def load_municipios(request):
    depto_id = request.GET.get('depto_id')  # Obtener la ID de la marca desde la solicitud Ajax
    print(depto_id)
    municipios = munic.objects.filter(cod_depto=depto_id).order_by('descrip_corta')  # Filtrar modelos por marca
    return JsonResponse(list(municipios.values('id', 'descrip_corta')), safe=False)


def load_cv(request):
    cod_munic = request.GET.get('cod_munic')  # Obtener la ID de la marca desde la solicitud Ajax
    print(cod_munic)
    centros = cv.objects.filter(cod_munic=cod_munic).order_by('nom')  # Filtrar modelos por marca
    return JsonResponse(list(centros.values('id', 'nom')), safe=False)


def frm_princ_cv(request):
    cvs = cv.objects.all()
    context = {
        'cv' : cvs
    }
    return render(request, 'cv/form_gen_cv.html', context)
def frm_mapa(request):
    return render(request, 'cv/form_mapa.html')

def cargar_cv(request):
    if request.method == 'POST':
        cv.objects.all().delete()
        archivo_excel = request.FILES['archivo_excel']
        try:
            df = pd.read_excel(archivo_excel)
            for index, row in df.iterrows():
                cv.objects.create(
                    cod_depto=depto.objects.get(id=row['Departamento']),
                    cod_munic=munic.objects.get(id=row['Municipio']),                    
                    latitud=row['Latitud'],
                    longitud=row['Longitud'],
                    nom=row['Nombre'],
                    procedencia=procedencia.objects.get(id=row['Unidad'])
                )
            return HttpResponse("Centro de Votacion Cargados Correctamente")
        except Exception as e:
            return HttpResponse(f"Error al cargar los centro de votacion: {e}")
    return render(request, 'cv/cargar_cv.html')

def cargar_guia(request):
    if request.method == 'POST':
        cv.objects.all().delete()
        archivo_excel = request.FILES['archivo_excel']
        try:
            df = pd.read_excel(archivo_excel)
            for index, row in df.iterrows():
                try:
                    cv.objects.create(
                        cod_depto=depto.objects.get(id=row['cod_depto']),
                        cod_munic=munic.objects.get(cod_munic=row['cod_munic']),
                        cod_area=area.objects.get(id=row['cod_area']),
                        latitud=row['latitud'],
                        longitud=row['longitud'],
                        sector_electoral=row['sector_electoral'],
                        carga_electoral=str(row['carga_electoral']),
                        nom=row['nom'],
                        cod_estado=estado.objects.get(id=row['cod_estado'])
                    )
                except Exception as fila_error:
                    print(f"Error en la fila {index + 2}: {fila_error}")
                    return HttpResponse(f"Error en la fila {index + 2}: {fila_error}")
            return HttpResponse("Centro de Votación cargados correctamente")
        except Exception as e:
            return HttpResponse(f"Error al procesar el archivo: {e}")
    return render(request, 'cv/cargar_guia_telefonica.html')

def guia_tel(request):
    if request.method == 'GET':
        contactos = Contacto.objects.all()
        return render(request, 'cv/form_guia_telefonica.html', {'contactos': contactos})
    
def registrar_manual(request):
    departamentos = depto.objects.all()
    return render(request, 'cv/form_registro.html', {'departamentos': departamentos})

def actualizar_cv(request):
    if request.method == 'POST':
        centro_id = request.POST.get('cv')
        estado_id = request.POST.get('estado')
        nueva_img = request.FILES.get('imagen')
        print(centro_id )
        print(nueva_img)
        print(estado_id)
        try:
            centro = get_object_or_404(cv, id=centro_id)
            if estado_id:
                centro.cod_estado = get_object_or_404(estado, id=estado_id)
            if nueva_img:
                centro.img = nueva_img
            centro.save()
            return JsonResponse({'mensaje': 'Centro actualizado correctamente'})
        except Exception as e:
            return JsonResponse({'error': f'Error al actualizar: {e}'}, status=500)
    return JsonResponse({'error': 'Método no permitido'}, status=405)