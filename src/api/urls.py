from django.urls import path, include
from django.views.generic import RedirectView

from rest_framework import routers
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from api import viewsets, views

router = routers.DefaultRouter()
router.register('users', viewsets.UserViewSet, basename='user')
router.register('entries', viewsets.EntryViewSet, basename='entries')

urlpatterns = [
    path('', RedirectView.as_view(url='/api/doc/')),
    path('auth/', include('account.urls')),
    path('tranlsations/', include('translations.urls')),
    path('health/', views.HealthCheckView.as_view(), name='health_check'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('doc/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path(
        'templates/<slug:id>/',
        views.GetTemplateView.as_view(),
        name='get_template',
    ),
]

urlpatterns += router.urls
