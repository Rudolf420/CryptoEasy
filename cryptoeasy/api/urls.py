from django.urls import path

from . import views

urlpatterns = [
    path('register', views.register),
    path('delete', views.delete),
    path('login', views.login),
    path('deposit', views.deposit),
    path('buy', views.buy),
    path('sell', views.sell),
    path('info', views.info)
]