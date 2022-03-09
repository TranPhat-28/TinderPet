from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('send/', views.updateMessage),
    path('fetch/', views.fetchAll),
    ]
