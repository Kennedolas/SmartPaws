# ==========================================
# produtos/urls.py
# ==========================================

from django.urls import path
from . import views

app_name = 'produtos'

urlpatterns = [
    # Lista de produtos (com filtros)
    path('', views.ProdutoListView.as_view(), name='lista'),
    
    # Detalhe do produto
    path('<slug:slug>/', views.ProdutoDetailView.as_view(), name='detalhe'),
    
    # Busca de produtos (opcional, se quiser rota separada)
    path('buscar/', views.ProdutoListView.as_view(), name='buscar'),
    
    # Filtrar por categoria (opcional)
    path('categoria/<slug:categoria_slug>/', views.ProdutoListView.as_view(), name='por_categoria'),
]
