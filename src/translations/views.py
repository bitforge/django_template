from collections import OrderedDict

from django.conf import settings

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import APIException

# from drf_spectacular.types import OpenApiTypes
# from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.utils import extend_schema

from translations import models
from translations import serializers


def get_translations(lang: str):
    """
    Build translsations dict for given language
    """
    texts = OrderedDict()
    for group in models.Group.objects.prefetch_related('texts'):
        for text in group.texts.all():
            value = getattr(text, lang, None)
            if value:
                if group.key not in texts:
                    texts[group.key] = OrderedDict()
                texts[group.key][text.key] = value
    return texts


class TranslationsView(generics.ListAPIView):
    queryset = models.Text.objects.none()
    serializer_class = serializers.GroupedTextsSerializer
    permission_classes = []
    authentication_classes = []

    @extend_schema(
        # Approach #1: Does not replace `lang` parameter in OpenApi schema.
        # parameters=[
        #     OpenApiParameter(
        #         name='lang',
        #         type=OpenApiTypes.STR,
        #         location=OpenApiParameter.QUERY,
        #         enum=settings.TRANSLATION_LANGUAGES,
        #         required=True,
        #     )
        # ],


        # Approach #2: Does not replace `lang` parameter in OpenApi schema either.
        parameters=[serializers.LangSerializer],
    )
    def get(self, request, lang: str):
        """
        Get all translations for language.
        """
        # Get supported language or fallback to 'de'
        # lang = request.GET.get('lang', 'de')
        if lang not in settings.TRANSLATION_LANGUAGES:
            raise APIException(f'Unsupported language: {lang}')
        texts = get_translations(lang)
        return Response(texts)
