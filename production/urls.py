from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from production import views

urlpatterns = [
    path('', views.UserCreate.as_view(), name=views.UserCreate.name),
    path('profile', views.ProfileView.as_view(), name=views.ProfileView.name),
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]
