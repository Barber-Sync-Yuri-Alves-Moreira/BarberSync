

from django.urls import path
from . import views

urlpatterns = [
    #
    path('', views.lista_barbeiros, name='lista_barbeiros'),

    
    path('servicos/<int:barbeiro_id>/', views.lista_servicos, name='lista_servicos'),
]