from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('check/', views.queryNextUser),
    path('like/', views.likeAndQueryNext),
]
