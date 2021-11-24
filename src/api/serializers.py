from rest_framework import serializers

from account import models as accounts


class ErrorDescriptionSerializer(serializers.Serializer):
    status = serializers.IntegerField(min_value=300, max_value=500)
    code = serializers.CharField(max_length=50)
    title = serializers.CharField(max_length=50)
    description = serializers.CharField()

    class Meta:
        fields = ('status', 'code', 'title', 'description')

    def __init__(self, instance=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if instance:
            self.instance = {
                'status': instance.status_code,
                'code': getattr(instance, 'code', instance.default_code),
                'title': getattr(instance, 'title', instance.default_detail),
                'description': getattr(instance, 'description', 'Not Provided.')
            }

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
