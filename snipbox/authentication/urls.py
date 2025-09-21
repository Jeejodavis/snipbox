from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import MyTokenObtainPairView, LogoutAndBlacklistRefreshTokenForUserView

urlpatterns = [
    path("login/", MyTokenObtainPairView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("logout/", LogoutAndBlacklistRefreshTokenForUserView.as_view(), name="logout"),
]
