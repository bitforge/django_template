from django.urls import path

from rest_framework import routers

from api import viewsets, tokens

router = routers.DefaultRouter()
router.register('users', viewsets.UserViewSet, basename='user')

urlpatterns = [
    path('auth/', tokens.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', tokens.TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/verify/', tokens.TokenVerifyView.as_view(), name='token_verify'),
]

urlpatterns += router.urls
