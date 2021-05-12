from django.urls import path
from . import views

app_name = 'myapp'
urlpatterns = [
    path('', views.home, name='home'),
    path('find_food', views.find_food, name='find_food'),
]