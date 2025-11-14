from django.urls import path
from . import views

app_name = 'carrinho'

urlpatterns = [
    # Carrinho
    path('', views.visualizar_carrinho, name='visualizar'),
    path('adicionar/<int:produto_id>/', views.adicionar_ao_carrinho, name='adicionar'),
    path('atualizar/<int:item_id>/', views.atualizar_quantidade, name='atualizar'),
    path('remover/<int:item_id>/', views.remover_item, name='remover'),
    path('limpar/', views.limpar_carrinho, name='limpar'),
    
    # Checkout
    path('checkout/', views.checkout, name='checkout'),
    path('finalizar/', views.finalizar_pedido, name='finalizar'),
    path('confirmado/<int:pedido_id>/', views.pedido_confirmado, name='pedido_confirmado'),
    
    # Pedidos
    path('pedidos/', views.meus_pedidos, name='meus_pedidos'),
    path('pedidos/<int:pedido_id>/', views.detalhe_pedido, name='detalhe_pedido'),
    
    # AJAX
    path('api/count/', views.carrinho_count, name='count'),
]