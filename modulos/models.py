import os
from uuid import uuid4
from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth.models import User

def camb_nom_arch(instance, filename):
    extension = os.path.splitext(filename)[1]
    nuevo_nombre = f"{uuid4().hex}{extension}"
    carpeta_destino = "Incidencias/"
    return os.path.join(carpeta_destino, nuevo_nombre)

class procedencia(models.Model):
    id = models.AutoField(primary_key=True)
    descrip_corta = models.TextField()    
    descrip_larga = models.TextField()    
    cod_proced_superior = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategorias')
    def __str__(self):
        fila =  str(self.descrip_corta)
        return fila
    
class depto(models.Model):
    id = models.AutoField(primary_key=True)
    descrip_corta = models.TextField()
    def __str__(self):
        fila = str(self.id) + "-" + str(self.descrip_corta) 
        return fila

class munic(models.Model):
    id = models.AutoField(primary_key=True)
    cod_munic = models.TextField(null=True)
    descrip_corta = models.TextField()
    cod_depto = models.ForeignKey(depto, on_delete=models.CASCADE, null=True, blank=True, related_name='subcategorias')
    def __str__(self):
        fila = str(self.cod_depto) + "-" +str(self.id) + "-" +str(self.descrip_corta)
        return fila
    
class estado(models.Model):
    id = models.AutoField(primary_key=True)
    descrip_corta = models.TextField()
    def __str__(self):
        fila = str(self.descrip_corta) 
        return fila

class area(models.Model):
    id = models.AutoField(primary_key=True)
    descrip_corta = models.TextField()
    def __str__(self):
        fila = str(self.id) + "-" + str(self.descrip_corta) 
        return fila
    
class cv(models.Model):
    id = models.AutoField(primary_key=True)
    cod_depto = models.ForeignKey(depto, on_delete=models.CASCADE, null=True)
    cod_munic = models.ForeignKey(munic, on_delete=models.CASCADE, null=True)
    cod_area = models.ForeignKey(area, on_delete=models.CASCADE, null=True)
    cod_estado = models.ForeignKey(estado, on_delete=models.CASCADE, null=True)
    longitud = models.FloatField(null = True)
    latitud = models.FloatField(null = True)
    sector_electoral = models.TextField(blank=True, null=True)
    carga_electoral = models.TextField(null = True)
    nom = models.TextField(blank=True, null=True)
    procedencia = models.ForeignKey(procedencia, on_delete=models.CASCADE, null=True)
    img = models.FileField(upload_to=camb_nom_arch, null = True, blank= True)

class Contacto(models.Model):
    no = models.IntegerField(null=True, blank=True, unique=True)
    depto = models.CharField(max_length=100)
    munic  = models.CharField(max_length=100)
    cv = models.CharField(max_length=100)
    grado1 = models.CharField(max_length=100)
    nom1 = models.CharField(max_length=100)
    num1= models.CharField(max_length=100)
    grado2 = models.CharField(max_length=100)
    nom2 = models.CharField(max_length=100)
    num2= models.CharField(max_length=100)

class contactoxcv(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    num= models.CharField(max_length=100)
    img = models.FileField(upload_to=camb_nom_arch, null = True, blank= True)
    cod_cv = models.ForeignKey(cv, on_delete=models.CASCADE, null=True)

class Munic_Geo(models.Model):
    nombre = models.CharField(max_length=100)
    shapeid = models.CharField(max_length=50)
    cod_munic = models.ForeignKey(munic, on_delete=models.CASCADE, null=True)
    cod_depto = models.ForeignKey(depto, on_delete=models.CASCADE, null=True)
    geom = models.MultiPolygonField()


class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    unidad_militar = models.ForeignKey(procedencia, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.usuario.username
    

class Guia_Telefonica(models.Model):
    no = models.IntegerField(null=True, blank=True, unique=True)
    grado = models.CharField(max_length=100)
    nom_ape  = models.CharField(max_length=100)
    fuerza = models.CharField(max_length=100)
    unidad = models.CharField(max_length=100)
    cargo_actual = models.CharField(max_length=100)
    tel_oficina = models.CharField(max_length=100)
    tel_ip = models.CharField(max_length=100)
    tel_celular = models.CharField(max_length=100)
    correo_inst = models.CharField(max_length=100)
    correo_personal = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.grado} {self.nombre} {self.apellido} - {self.cargo_actual}"
    