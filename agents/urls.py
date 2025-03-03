from django.urls import path
from .views import get_cities

urlpatterns = [
    path("api/get-cities/", get_cities, name="get-cities"),
]
