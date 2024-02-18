from django.conf import settings

from rest_framework import serializers


class LangSerializer(serializers.Serializer):
    lang = serializers.ChoiceField(required=True, choices=settings.TRANSLATION_LANGUAGES)


class GroupedTextsSerializer(serializers.Serializer):
    key = serializers.JSONField()
