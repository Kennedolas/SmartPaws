

from django.apps import AppConfig


class PagamentoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pagamento'
from django.contrib import admin
from django.utils.html import format_html
from .models import Endereco, Pedido, ItemPedido, Pagamento, RastreamentoEntrega


@admin.register(Endereco)
class EnderecoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'endereco', 'numero', 'cidade', 'estado', 'principal']
    list_filter = ['principal', 'estado', 'data_cadastro']
    search_fields = ['usuario__username', 'endereco', 'cidade', 'cep']
    list_editable = ['principal']


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0
    readonly_fields = ['subtotal']


class PagamentoInline(admin.StackedInline):
    model = Pagamento
    extra = 0
    readonly_fields = ['data_criacao', 'data_aprovacao']


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = [
        'numero_pedido', 'usuario', 'total', 'status_badge',
        'data_pedido', 'total_itens_display'
    ]
    
    list_filter = ['status', 'data_pedido', 'data_pagamento']
    search_fields = ['numero_pedido', 'usuario__username', 'usuario__email']
    readonly_fields = [
        'numero_pedido', 'uuid', 'data_pedido',
        'data_pagamento', 'data_envio', 'data_entrega'
    ]
    
    inlines = [ItemPedidoInline, PagamentoInline]
    
    fieldsets = (
        ('Identificação', {
            'fields': ('numero_pedido', 'uuid', 'usuario')
        }),
        ('Endereço de Entrega', {
            'fields': ('endereco_entrega',)
        }),
        ('Valores', {
            'fields': ('subtotal', 'taxa_entrega', 'desconto', 'total')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Datas', {
            'fields': ('data_pedido', 'data_pagamento', 'data_envio', 'data_entrega')
        }),
        ('Observações', {
            'fields': ('observacoes',)
        }),
    )
    
    def status_badge(self, obj):
        colors = {
            'pendente': '#ffc107',
            'aguardando_pagamento': '#17a2b8',
            'pago': '#28a745',
            'em_separacao': '#007bff',
            'enviado': '#6610f2',
            'entregue': '#28a745',
            'cancelado': '#dc3545',
            'reembolsado': '#6c757d',
        }
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 10px; border-radius: 3px; font-weight: bold;">{}</span>',
            colors.get(obj.status, '#6c757d'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def total_itens_display(self, obj):
        return obj.total_itens
    total_itens_display.short_description = 'Total de Itens'
    
    actions = ['marcar_como_pago', 'marcar_como_enviado', 'cancelar_pedidos']
    
    def marcar_como_pago(self, request, queryset):
        from django.utils import timezone
        count = queryset.filter(status='aguardando_pagamento').update(
            status='pago',
            data_pagamento=timezone.now()
        )
        self.message_user(request, f'{count} pedido(s) marcado(s) como pago.')
    marcar_como_pago.short_description = 'Marcar como Pago'
    
    def marcar_como_enviado(self, request, queryset):
        from django.utils import timezone
        count = queryset.filter(status='em_separacao').update(
            status='enviado',
            data_envio=timezone.now()
        )
        self.message_user(request, f'{count} pedido(s) marcado(s) como enviado.')
    marcar_como_enviado.short_description = 'Marcar como Enviado'
    
    def cancelar_pedidos(self, request, queryset):
        count = queryset.filter(status__in=['pendente', 'aguardando_pagamento']).update(
            status='cancelado'
        )
        self.message_user(request, f'{count} pedido(s) cancelado(s).')
    cancelar_pedidos.short_description = 'Cancelar Pedidos'


@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ['pedido', 'nome_produto', 'quantidade', 'preco_unitario', 'subtotal']
    list_filter = ['pedido__status', 'pedido__data_pedido']
    search_fields = ['pedido__numero_pedido', 'nome_produto']


@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display = [
        'pedido', 'forma_pagamento', 'valor', 'status_badge', 'data_criacao'
    ]
    
    list_filter = ['forma_pagamento', 'status', 'data_criacao']
    search_fields = ['pedido__numero_pedido', 'transaction_id']
    
    readonly_fields = ['data_criacao', 'data_aprovacao', 'data_cancelamento']
    
    def status_badge(self, obj):
        colors = {
            'pendente': '#ffc107',
            'processando': '#17a2b8',
            'aprovado': '#28a745',
            'recusado': '#dc3545',
            'cancelado': '#6c757d',
            'reembolsado': '#fd7e14',
        }
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            colors.get(obj.status, '#6c757d'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'


@admin.register(RastreamentoEntrega)
class RastreamentoEntregaAdmin(admin.ModelAdmin):
    list_display = ['pedido', 'status', 'localizacao', 'data_hora']
    list_filter = ['data_hora']
    search_fields = ['pedido__numero_pedido', 'status']
