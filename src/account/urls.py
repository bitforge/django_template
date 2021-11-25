from django.urls import path

from account import views

urlpatterns = [
    path('login/', views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', views.TokenRefreshView.as_view(), name='token_refresh'),
    path('verify/', views.TokenVerifyView.as_view(), name='token_verify'),\
    path('google/', views.GoogleAuthView.as_view(), name='token_google'),
    path('password/reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password/reset/confirm/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]