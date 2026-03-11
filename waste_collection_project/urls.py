"""
Root URL Configuration for Waste Collection Project
"""
from django.urls import path, include

urlpatterns = [
    # All app URLs are handled by waste_management app
    path('', include('waste_management.urls')),
]
