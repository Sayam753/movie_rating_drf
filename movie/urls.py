from django.urls import path
from movie import views

urlpatterns = [
    path('', views.MovieListCreateView.as_view(), name=views.MovieListCreateView.name),
    path('rate', views.RateCreateView.as_view(), name=views.RateCreateView.name),
]
