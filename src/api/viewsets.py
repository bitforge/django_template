from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api import serializers

from account import models as accounts


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = accounts.User.objects.all()
    serializer_class = serializers.UserSerializer

    @action(methods=['get'], detail=False)
    def me(self, request):
        """ Show details of the user currently logged in. """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        """ Lists all users. """
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """ Details of a single user. """
        return super().retrieve(request, *args, **kwargs)
