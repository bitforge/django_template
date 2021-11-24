from django.urls import path

from account import views

urlpatterns = [
    path('', views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', views.TokenRefreshView.as_view(), name='token_refresh'),
    path('verify/', views.TokenVerifyView.as_view(), name='token_verify'),
]