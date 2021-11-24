from django.urls import path, include
from django.views.generic import RedirectView

from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from api import viewsets, views

router = routers.DefaultRouter()
router.register('users', viewsets.UserViewSet, basename='user')

urlpatterns = [
    path('', RedirectView.as_view(url='/api/doc/')),
    path('auth/', include('account.urls')),
    path('health/', views.HealthCheckView.as_view(), name='health_check'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('doc/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

urlpatterns += router.urls
