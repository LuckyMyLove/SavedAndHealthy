from django.urls import path
from . import views


urlpatterns = [
    path('', views.find_food, name='find_food'),
]