from django.urls import path

from usuarios import views

urlpatterns = [
    path('logar/', views.logar, name='logar'),
    path('cadastro/', views.cadastro, name='cadastro'),
]
