from django.utils.translation import ugettext_lazy as _

from rest_framework import generics
from rest_framework.response import Response

from app import models
from api import serializers, health


class HealthCheckView(generics.GenericAPIView):
    queryset = models.User.objects.none()
    serializer_class = serializers.HealthStatusSerializer
    permission_classes = []
    authentication_classes = []

    def get(self, request, format=None):
        """
        Check health status of required subsystems.
        """
        checks = {
            'db_up': health.check_db(),
            'storage_up': health.check_storage(),
            'cache_up': health.check_cache()
        }
        status_code = 200 if all(checks.values()) else 503
        return Response(checks, status=status_code)

