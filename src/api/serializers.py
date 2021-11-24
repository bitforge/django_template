from rest_framework import serializers

from account import models as accounts


class HealthStatusSerializer(serializers.Serializer):
    db_up = serializers.BooleanField()
    storage_up = serializers.BooleanField()
    cache_up = serializers.BooleanField()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = accounts.User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'date_joined',
        ]
