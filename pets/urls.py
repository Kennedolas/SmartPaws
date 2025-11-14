# ==========================================
# pets/urls.py
# ==========================================

from django.urls import path
from . import views

app_name = 'pets'

urlpatterns = [
    # Página principal de adoção
    path('', views.adocao, name='adocao'),
    
    # Detalhes do pet
    path('<slug:slug>/', views.detalhe_pet, name='detalhe'),
    
    # Solicitar adoção
    path('<slug:slug>/solicitar/', views.solicitar_adocao, name='solicitar'),
    
    # Minhas solicitações
    path('minhas/solicitacoes/', views.minhas_solicitacoes, name='minhas_solicitacoes'),
    
    # Busca
    path('buscar/', views.buscar_pets, name='buscar'),
    
    # Promoções
    path('promocoes/', views.promocoes_adocao, name='promocoes'),
    path('promocoes/<slug:slug>/', views.detalhe_promocao, name='promocao_detalhe'),
]
