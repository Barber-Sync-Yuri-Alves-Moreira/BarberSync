from django.urls import path
from . import views

urlpatterns = [

    path('', views.lista_barbeiros, name='lista_barbeiros'),
    path('servicos/<int:barbeiro_id>/', views.lista_servicos, name='lista_servicos'),
    path('agendar/<int:barbeiro_id>/<int:servico_id>/', 
         views.selecionar_data, name='selecionar_data'),
    path('agendar/<int:barbeiro_id>/<int:servico_id>/<str:data>/', 
         views.selecionar_horario, name='selecionar_horario'),
]