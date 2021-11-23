from rest_framework import serializers

from app import models


class HealthStatusSerializer(serializers.Serializer):
    db_up = serializers.BooleanField()
    storage_up = serializers.BooleanField()
    cache_up = serializers.BooleanField()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'date_joined',
            'is_active',
            'is_staff',
            'is_superuser',
        ]
