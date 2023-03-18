
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView

from account import models as accounts
from api import serializers, health
from {{ project_name }} import models


class HealthCheckView(generics.GenericAPIView):
    queryset = accounts.User.objects.none()
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
            'cache_up': health.check_cache(),
        }
        status_code = 200 if all(checks.values()) else 503
        return Response(checks, status=status_code)


class GetTemplateView(RetrieveAPIView):
    queryset = models.Template.objects.all()
    serializer_class = serializers.TemplateSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'

    def get(self, request, *args, **kwargs):
        """
        Get markdown template by ID.
        """
        return super().get(request, *args, **kwargs)
