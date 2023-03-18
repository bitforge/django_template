from django.urls import path

from translations import views

urlpatterns = [
    path('export/pwa', views.export_pwa, name='trans-export-pwa'),
]
