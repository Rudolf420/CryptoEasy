from django.urls import path

from . import views

urlpatterns = [
    path('register', views.register),
    path('delete', views.delete),
    path('login', views.login),
]