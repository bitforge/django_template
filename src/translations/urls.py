from django.urls import path

from translations import views

urlpatterns = [
    # Failed approach: annotate GET parameter with regex to annotate OpenApi schema.
    # re_path(r'(?P<lang>[de|en])/', views.TranslationsView.as_view(), name='get-translations'),

    # Parameters: <str:lang>, required, enum: `settings.TRANSLATION_LANGUAGES`
    path('', views.TranslationsView.as_view(), name='get-translations'),
]
