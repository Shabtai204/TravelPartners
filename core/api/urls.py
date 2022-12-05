from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_routes),
    path('trips/',  views.get_trips),
    path('trips/<str:pk>',  views.get_trip)
]