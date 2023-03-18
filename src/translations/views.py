from collections import OrderedDict

from rest_framework import generics
from rest_framework.response import Response

from translations import models
from translations import serializers


def get_translations(lang: str):
    """
    Build translsations dict for language
    """
    texts = OrderedDict()
    for group in models.Group.objects.prefetch_related('texts'):
        for text in group.texts.all():
            text = getattr(text, lang, None)
            if text:
                group_key = text.group.key
                text_key = text.key
                if group_key not in texts:
                    texts[group_key] = OrderedDict()
                texts[group_key][text_key] = text
    return texts


class TranslationsView(generics.ListAPIView):
    queryset = models.Text.objects.none()
    serializer_class = serializers.TextSerializer
    permission_classes = []
    authentication_classes = []

    def get(self, request, lang):
        """
        Get all translations for language.
        """
        texts = get_translations(lang)
        return Response(texts)
