from django.urls import path

from translations import views

urlpatterns = [
    path('<str:lang>', views.TranslationsView.as_view(), name='get-translations'),
]
