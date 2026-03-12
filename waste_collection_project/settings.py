"""
Django Settings for Waste Collection Scheduling Management System
Uses MongoDB via MongoEngine for document storage
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-waste-collection-secret-key-change-in-production'

DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'waste_management',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'waste_collection_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'waste_collection_project.wsgi.application'

# MongoDB Connection Settings (MongoEngine)
MONGODB_SETTINGS = {
    'db': 'waste_collection_db',
    'host': 'localhost',
    'port': 27017,
}

# Use dummy DB backend since we use MongoEngine directly (not Django ORM)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.dummy',
    }
}

# Static Files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media Files (for complaint image uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Google Maps API Key
GOOGLE_MAPS_API_KEY = 'AIzaSyDLboNMvYIpzqcpjIK9ybVd3x22SjiogPM'
