import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure--8oem^&3zf-+y5n%c#n+wjv7^4kn@8_l(0q+05&-s65#f-q+d('

# SECURITY WARNING: sdon't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', '172.22.16.16', '172.22.2.10','ejercito.ffaa.mil.hn']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'leaflet',
    'modulos',
]

LEAFLET_CONFIG = {
    'DEFAULT_CENTER': (14.6, -86.8),  # Centro aproximado de Honduras
    'DEFAULT_ZOOM': 7,
    'MIN_ZOOM': 6,
    'MAX_ZOOM': 12,
}

GDAL_LIBRARY_PATH = r"C:\OSGeo4W\bin\gdal310.dll"  # usa la ruta real de tu archivo
GEOS_LIBRARY_PATH = r"C:\OSGeo4W\bin\geos_c.dll"   # Ruta real de la DLL de GEOS
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'multiplataforma.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'multiplataforma.wsgi.application'
""" 
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'multiplataforma',
        'USER': 'sa',
        'PASSWORD': 'T3cn0l0g1@13',
        'HOST': '172.22.4.16',
        'PORT': '',
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
                     },
    }
} """
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'multiplataforma',
        'USER': 'postgres',
        'PASSWORD': 'Tecnologia13',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/


STATIC_URL = 'static/'
MEDIA_URL = '/media/'  # URL de acceso a los archivos cargados
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
