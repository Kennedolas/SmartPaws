from django.contrib import admin
from .models import Carrinho, ItemCarrinho, Pedido, ItemPedido


class ItemCarrinhoInline(admin.TabularInline):
    model = ItemCarrinho
    extra = 0
    readonly_fields = ['preco_unitario', 'total']


@admin.register(Carrinho)
class CarrinhoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'total_itens', 'subtotal', 'created_at']
    search_fields = ['usuario__email', 'usuario__first_name']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [ItemCarrinhoInline]


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0
    readonly_fields = ['nome_produto', 'quantidade', 'preco_unitario', 'subtotal']


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['numero_pedido', 'usuario', 'status', 'forma_pagamento', 'total', 'created_at']
    list_filter = ['status', 'forma_pagamento', 'created_at']
    search_fields = ['numero_pedido', 'usuario__email', 'usuario__first_name']
    readonly_fields = ['numero_pedido', 'created_at', 'updated_at', 'pago_em']
    inlines = [ItemPedidoInline]
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('numero_pedido', 'usuario', 'status')
        }),
        ('Valores', {
            'fields': ('subtotal', 'desconto', 'frete', 'total')
        }),
        ('Entrega', {
            'fields': ('endereco_entrega',)
        }),
        ('Pagamento', {
            'fields': ('forma_pagamento', 'payment_id', 'qr_code_pix')
        }),
        ('Observações', {
            'fields': ('observacoes',)
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at', 'pago_em')
        }),
    )