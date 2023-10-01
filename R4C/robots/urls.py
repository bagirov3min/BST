from django.urls import path
from . import views

urlpatterns = [
    path('add_robot/', views.add_robot, name='add_robot'),
]