import json, os, gc, shutil, tempfile, traceback, zipfile, pandas as pd
from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from django.db.models import Count, Sum
from django.db.models.functions import Cast
from django.db.models import IntegerField
from django.contrib import messages
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon, Polygon
from django.contrib.gis.serializers import geojson
from django.core.serializers import serialize
from .models import *
from .forms import ShapefileUploadForm
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

list_deptos = depto.objects.all()
list_munic = munic.objects.all()




@login_required
def inicio_2(request):
    return render(request, 'core/base.html')

def rpt_info_gen(request):
    estado_data = cv.objects.values('cod_estado__descrip_corta').annotate(total=Count('id')).order_by('cod_estado__descrip_corta')
    labels_estado = [item['cod_estado__descrip_corta'] for item in estado_data]
    data_estado = [item['total'] for item in estado_data]

    # Datos por departamento
    depto_data = cv.objects.values('cod_depto__descrip_corta').annotate(total=Count('id')).order_by('cod_depto__descrip_corta')
    labels_depto = [item['cod_depto__descrip_corta'] for item in depto_data]
    data_depto = [item['total'] for item in depto_data]
    
    depto_data = (
        cv.objects
        .annotate(carga_int=Cast('carga_electoral', IntegerField()))
        .values('cod_depto__descrip_corta')
        .annotate(total_carga=Sum('carga_int'))
        .order_by('-total_carga')
    )
    
    labels = [item['cod_depto__descrip_corta'] for item in depto_data]
    data = [item['total_carga'] for item in depto_data]
    
    context = {
        'labels_estado': labels_estado,
        'data_estado': data_estado,
        'labels_depto': labels_depto,
        'data_depto': data_depto,
        'labels_carga': labels,
        'data_carga': data,
    }  
    return render(request, 'cv/reportes/rpt_info_gen.html',context )

def rpt_info_situacion(request):
    estado_data = cv.objects.values('cod_estado__descrip_corta').annotate(total=Count('id')).order_by('cod_estado__descrip_corta')
    labels_estado = [item['cod_estado__descrip_corta'] for item in estado_data]
    data_estado = [item['total'] for item in estado_data]

    context = {
        'labels_estado': labels_estado,
        'data_estado': data_estado,
    }  
    return render(request, 'cv/reportes/rpt_info_situacion.html',context )

def load_municipios(request):
    depto_id = request.GET.get('depto_id')  # Obtener la ID de la marca desde la solicitud Ajax
    municipios = munic.objects.filter(cod_depto=depto_id).order_by('descrip_corta')  # Filtrar modelos por marca
    return JsonResponse(list(municipios.values('id', 'descrip_corta')), safe=False)

def load_cv(request):
    cod_munic = request.GET.get('cod_munic')  # Obtener la ID de la marca desde la solicitud Ajax
    centros = cv.objects.filter(cod_munic=cod_munic).order_by('nom')  # Filtrar modelos por marca
    return JsonResponse(list(centros.values('id', 'nom')), safe=False)

def frm_princ_cv(request):
    if request.user.is_superuser:
        cvs = cv.objects.all().order_by('id')
    else:
        perfil = PerfilUsuario.objects.get(usuario=request.user)
        cvs = cv.objects.filter(procedencia=perfil.unidad_militar)
    context = {
        'cv' : cvs
    }
    return render(request, 'cv/form_gen_cv.html', context)

def frm_adminxunidad_cv(request):
    if request.user.is_superuser:
        cvs = cv.objects.all().order_by('id')
    else:
        perfil = PerfilUsuario.objects.get(usuario=request.user)
        cvs = cv.objects.filter(procedencia=perfil.unidad_militar).order_by('id')
    context = {
        'cv' : cvs
    }
    return render(request, 'cv/form_admin_cv.html', context)

def frm_mapa(request):
    return render(request, 'cv/form_mapa.html')

def cargar_contactos(request):
    if request.method == 'POST':
        Guia_Telefonica.objects.all().delete()
        # Obtenemos el archivo subido
        archivo_excel = request.FILES['archivo_excel']
        
        # Leemos el archivo Excel con pandas
        try:
            df = pd.read_excel(archivo_excel)
            # Iteramos sobre las filas del DataFrame
            for index, row in df.iterrows():
                # Crear el contacto en la base de datos
                Guia_Telefonica.objects.create(
                    no=row['no'],
                    grado=row['grado'],
                    nom_ape=row['nom_ape'],
                    fuerza=row['fuerza'],
                    unidad=row['unidad'],
                    cargo_actual=row['cargo_actual'],
                    tel_oficina=row['tel_oficina'],
                    tel_ip=row['tel_ip'],
                    tel_celular=row['tel_celular'],
                    correo_inst=row['correo_inst'],
                    correo_personal=row['correo_personal']
                )
            return HttpResponse("Contactos cargados correctamente")
        except Exception as e:
            return HttpResponse(f"Error al cargar los contactos: {e}")
    return render(request, 'cv/cargar_contactos.html')

def cargar_cv(request):
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
    return render(request, 'cv/cargar_contactos.html')

def guia_tel(request):
    if request.method == 'GET':
        contactos = Guia_Telefonica.objects.all()
        return render(request, 'cv/form_guia_telefonica.html', {'contactos': contactos})

def guia_tel_cv(request):
    if request.method == 'GET':
        contactos = contactoxcv.objects.all()
        return render(request, 'cv/form_guia_telefonica_cv.html', {'contactos': contactos})
    
def registrar_manual(request):
    departamentos = depto.objects.all()
    return render(request, 'cv/form_registro.html', {'departamentos': departamentos})

def actualizar_cv(request):
    if request.method == 'POST':
        centro_id = request.POST.get('cv')
        estado_id = request.POST.get('estado')
        nueva_img = request.FILES.get('foto_cv')
        try:
            centro = get_object_or_404(cv, id=centro_id)
            if estado_id:
                centro.cod_estado = get_object_or_404(estado, id=estado_id)
            if nueva_img:
                centro.img = nueva_img
            centro.save()
            noms = request.POST.getlist('nombre_seguridad[]')
            tels = request.POST.getlist('telefono_seguridad[]')
            img_seguridad = request.FILES.getlist('foto_seguridad[]')
            for i in range(len(noms)):
                nombre = noms[i]
                telefono = tels[i]
                foto = img_seguridad[i] if i < len(img_seguridad) else None

                contacto = contactoxcv(
                nom=nombre,
                num=telefono,
                cod_cv=centro
                )
                if foto:
                    contacto.img = foto
                contacto.save()
            
            return redirect(f"{reverse('registrar_manual')}?exito=1")
        except Exception as e:
            return JsonResponse({'error': f'Error al actualizar: {e}'}, status=500)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def detalle_centro(request, centro_id):
    centro = cv.objects.get(id=centro_id)
    personal = contactoxcv.objects.filter(cod_cv=centro_id)

    return JsonResponse({
        "nombre": centro.nom,
        "departamento": centro.cod_depto.descrip_corta,
        "municipio": centro.cod_munic.descrip_corta,
        "sector": centro.sector_electoral,
        "carga": centro.carga_electoral,
        "foto_centro": centro.img.url if centro.img else "",
                "personal": [
            {
                "gradynom": p.nom,
                "telefono": p.num,
                "foto": p.img.url if p.img else ""
            }
            for p in personal
        ]
    })

def obtener_datos_cv(request):
    cv_id = request.GET.get('cv_id')
    try:
        centro = cv.objects.select_related('cod_estado').get(id=cv_id)
        contactos = contactoxcv.objects.filter(cod_cv=centro)

        contactos_data = []
        for c in contactos:
            contactos_data.append({
                'id': c.id,
                'nom': c.nom,
                'num': c.num,
                'img_url': c.img.url if c.img else '',
            })

        data = {
            'estado_id': centro.cod_estado.id if centro.cod_estado else '',
            'img_url': centro.img.url if centro.img else '',
            'personal': contactos_data,
        }
        return JsonResponse(data)
    except cv.DoesNotExist:
        return JsonResponse({'error': 'Centro no encontrado'}, status=404)

def eliminar_contacto(request):
    contacto_id = request.GET.get('id')
    try:
        contacto = contactoxcv.objects.get(pk=contacto_id)
        contacto.delete()
        return JsonResponse({'success': True})
    except contactoxcv.DoesNotExist:
        return JsonResponse({'error': 'Contacto no encontrado'}, status=404)

def cargar_shapefile(request):
    if request.method == 'POST':

        form = ShapefileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            archivo_zip = request.FILES['archivo']
            try:
                # Paso 1: Extraer el ZIP en un directorio temporal
                with tempfile.TemporaryDirectory() as tmpdirname:
                    zip_path = os.path.join(tmpdirname, archivo_zip.name)
                    with open(zip_path, 'wb') as f:
                        for chunk in archivo_zip.chunks():
                            f.write(chunk)

                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                        zip_ref.extractall(tmpdirname)

                    # Buscar el archivo .shp
                    shp_files = [f for f in os.listdir(tmpdirname) if f.endswith('.shp')]
                    if not shp_files:
                        messages.error(request, "No se encontró ningún archivo .shp.")
                        return redirect('cargar_shapefile')

                    base_name = shp_files[0][:-4]

                    # Paso 2: Copiar todos los archivos del shapefile a otra carpeta (fuera del `with`)
                    tmp_copy_dir = tempfile.mkdtemp()
                    for ext in ['.shp', '.shx', '.dbf', '.prj', '.cpg']:
                        src_file = os.path.join(tmpdirname, base_name + ext)
                        if os.path.exists(src_file):
                            shutil.copy(src_file, tmp_copy_dir)

                # Paso 3: Procesar el shapefile (fuera del bloque anterior)
                shp_path = os.path.join(tmp_copy_dir, base_name + '.shp')
                ds = DataSource(shp_path)
                layer = ds[0]

                for feat in layer:
                    nombre = feat.get('shapename') or 'Sin nombre'
                    shapeid = feat.get('shapeid')
                    geom = GEOSGeometry(feat.geom.geojson)

                    if isinstance(geom, Polygon):
                        geom = MultiPolygon(geom)

                    Munic_Geo.objects.create(nombre=nombre, geom=geom, shapeid=shapeid)

                # Liberar recursos antes de eliminar archivos
                del layer
                del ds
                gc.collect()

                # Limpiar carpeta temporal manualmente
                shutil.rmtree(tmp_copy_dir, ignore_errors=True)

                messages.success(request, "Shapefile cargado correctamente.")
                return redirect('cargar_shapefile')

            except Exception as e:
                error_completo = traceback.format_exc()
                messages.error(request, f"Ocurrió un error:\n{error_completo}")
                return redirect('cargar_shapefile')
    else:
        form = ShapefileUploadForm()
    return render(request, 'cv/cargar_shapefile.html', {'form': form})

def mapa_municipios(request):
    return render(request, 'cv/mapa_municipios.html')

def geojson_municipios(request):
    data = serialize(
        'geojson',
        Munic_Geo.objects.all(),
        geometry_field='geom',
        fields=('nombre', 'shapeid')
    )
    return JsonResponse(data, safe=False)

def geojson_departamento(request, departamento):
    # Filtramos municipios por el nombre del departamento (en cod_munic.depto)
    municipios = Munic_Geo.objects.filter(cod_munic__cod_depto=departamento)
    features = []

    for municipio in municipios:
        # Filtro de CV relacionados al municipio actual
        cvs = cv.objects.filter(cod_munic=municipio.cod_munic)

        # Conteo por estado (según cod_estado.descripcion)
        abiertos = cvs.filter(cod_estado=3).count()
        inactivos = cvs.filter(cod_estado=1).count()
        cerrados = cvs.filter(cod_estado=4).count()
        activos = cvs.filter(cod_estado=2).count()
        cod_municipio = str(municipio.cod_munic.cod_munic)

        # Construir cada feature tipo GeoJSON
        features.append({
            "type": "Feature",
            "geometry": json.loads(municipio.geom.geojson),
            "properties": {
                "nombre": municipio.nombre,
                "abiertos": abiertos,
                "inactivos": inactivos,
                "cerrados": cerrados,
                "activos": activos,
                "codmunicipio": cod_municipio
            }
        })

    geojson_data = {
        "type": "FeatureCollection",
        "features": features
    }

    return JsonResponse(geojson_data)
    
def mapa_departamento(request):
    departamentos = depto.objects.all()
    return render(request, 'cv/reportes/rpt_info_depto.html', {'departamentos': departamentos})

def centros_por_departamento(request, id_departamento):
    centros = cv.objects.filter(cod_munic__cod_depto=id_departamento)
    data = []
    for centro in centros:
        data.append({
            "nombre": centro.nom,
            "municipio": centro.cod_munic.descrip_corta,
            "lat": centro.latitud,
            "lng": centro.longitud,
            "estado": centro.cod_estado.descrip_corta
        })
    return JsonResponse(data, safe=False)

def centros_por_municipio(request, cod_municipio):
    centros = cv.objects.filter(cod_munic__cod_munic=cod_municipio)
    data = []
    for centro in centros:
        contactos = contactoxcv.objects.filter(cod_cv=centro)
        contactos_data = [
            {
                'nombre': c.nom,
                'numero': c.num,
                'imagen': c.img.url if c.img else None
            }
            for c in contactos
        ]
        print(contactos_data)
        data.append({
            'id': centro.id,
            'nombre': centro.nom,
            'estado': str(centro.cod_estado),
            'contactos': contactos_data
        })
    return JsonResponse(data, safe=False)

def obtener_personal_cv(request, centro_id):
    print("hola")
    if request.method == 'GET':
        contactos = contactoxcv.objects.filter(cod_cv=centro_id)
        personal = [

            {
                'id' : c.id,
                'nom': c.nom,
                'num': c.num,
                'img': c.img.url if c.img else None
            }
            for c in contactos
            
        ]
        print(personal)
        return JsonResponse(list(personal), safe=False)

@csrf_exempt
@require_http_methods(["POST"])
def agregar_personal_cv(request):
    if request.method == 'POST':
        try:
            # Acceder directamente desde POST y FILES
            centro_id = request.POST.get('centro_id')
            nombre = request.POST.get('nombre')
            telefono = request.POST.get('telefono')
            foto = request.FILES.get('foto')  # Aquí sí recibes el archivo real

            centro = cv.objects.get(id=centro_id)

            nuevo = contactoxcv.objects.create(
                cod_cv=centro,
                nom=nombre,
                num=telefono,
                img=foto  # El campo `img` debe ser un ImageField en el modelo
            )

            return JsonResponse({'status': 'ok', 'id': nuevo.id})
        
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Centro no encontrado'}, status=404)
        
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

@csrf_exempt
def eliminar_personal(request, id):
    if request.method == 'DELETE':
        try:
            personal = contactoxcv.objects.get(id=id)
            personal.delete()
            return JsonResponse({'status': 'ok'})
        except contactoxcv.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'No encontrado'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

def obtener_foto_cv(request, centro_id):
    try:
        centro = cv.objects.get(id=centro_id)
        url = centro.img.url if centro.img else ''
        return JsonResponse({'foto': url})
    except cv.DoesNotExist:
        return JsonResponse({'foto': ''})

@csrf_exempt
def guardar_foto_cv(request):
    if request.method == 'POST':
        centro_id = request.POST.get('centro_id')
        nueva_foto = request.FILES.get('nueva_foto')

        try:
            centro = cv.objects.get(id=centro_id)
            centro.img = nueva_foto
            centro.save()
            return JsonResponse({'status': 'ok'})
        except cv.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'CV no encontrado'}, status=404)
        
@csrf_exempt
def guardar_ubicacion_cv(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            centro = cv.objects.get(id=data['centro_id'])
            centro.latitud = data['lat']
            centro.longitud = data['lng']
            centro.save()
            return JsonResponse({'status': 'ok'})
        except cv.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Centro no encontrado'}, status=404)
        
@csrf_exempt
def actualizar_estado_cv(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data['id'])
            print(data['estado'])
            centro = cv.objects.get(id=data['id'])
            nuevo_estado = estado.objects.get(id=data['estado'])  # o tu modelo de estado
            centro.cod_estado = nuevo_estado
            centro.save()
            return JsonResponse({'status': 'ok'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)