# ==========================================
# servicos/urls.py
# ==========================================

from django.urls import path
from . import views

app_name = 'servicos'

urlpatterns = [
    # Lista de serviços
    path('', views.lista_servicos, name='lista'),
    
    # Detalhe do serviço
    path('servico/<slug:slug>/', views.detalhe_servico, name='detalhe'),
    
    # Agendar serviço
    path('servico/<slug:slug>/agendar/', views.agendar_servico, name='agendar'),
    
    # Meus agendamentos
    path('meus-agendamentos/', views.meus_agendamentos, name='meus_agendamentos'),
    
    # Prestadores
    path('prestadores/', views.lista_prestadores, name='prestadores'),
    path('prestadores/<slug:slug>/', views.detalhe_prestador, name='detalhe_prestador'),
]
