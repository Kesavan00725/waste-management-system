"""
Root URL Configuration for Waste Collection Project
"""
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # All app URLs are handled by waste_management app
    path('', include('waste_management.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
