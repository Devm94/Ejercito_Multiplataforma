from django import forms

class ShapefileUploadForm(forms.Form):
    archivo = forms.FileField(label="Subir archivo .zip con shapefile")