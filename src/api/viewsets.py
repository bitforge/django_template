from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api import serializers

from app import models


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

    @action(methods=['get'], detail=False)
    def me(self, request):
        """ Show details of the user currently logged in. """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        """ Lists all users that are members in the same projects. """
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """ Details of a single user. """
        return super().retrieve(request, *args, **kwargs)
