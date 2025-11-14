from django.contrib import admin
from django.utils.html import format_html
from .models import CategoriaProduto, Produto, ImagemProduto


@admin.register(CategoriaProduto)
class CategoriaProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'tipo', 'ordem', 'ativo', 'total_produtos']
    list_filter = ['tipo', 'ativo']
    search_fields = ['nome', 'descricao']
    list_editable = ['ordem', 'ativo']
    prepopulated_fields = {'slug': ('nome',)}
    
    def total_produtos(self, obj):
        return obj.produtos.count()
    total_produtos.short_description = 'Total de Produtos'


class ImagemProdutoInline(admin.TabularInline):
    model = ImagemProduto
    extra = 1
    fields = ['imagem', 'ordem']


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = [
        'imagem_thumb',
        'nome',
        'categoria',
        'preco_final_display',
        'desconto_display',
        'estoque',
        'avaliacao',
        'ativo'
    ]
    
    list_filter = ['categoria', 'ativo', 'destaque', 'novidade', 'created_at']
    search_fields = ['nome', 'descricao', 'marca']
    list_editable = ['ativo']
    prepopulated_fields = {'slug': ('nome',)}
    inlines = [ImagemProdutoInline]
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'slug', 'categoria', 'descricao', 'marca')
        }),
        ('Imagem', {
            'fields': ('imagem_principal',)
        }),
        ('Preços', {
            'fields': ('preco_original', 'preco_desconto')
        }),
        ('Estoque', {
            'fields': ('estoque', 'estoque_minimo')
        }),
        ('Avaliação', {
            'fields': ('avaliacao', 'numero_avaliacoes')
        }),
        ('Características', {
            'fields': ('peso_tamanho',)
        }),
        ('Destaque', {
            'fields': ('destaque', 'novidade', 'ativo')
        }),
    )
    
    def imagem_thumb(self, obj):
        if obj.imagem_principal:
            return format_html(
                '<img src="{}" width="50" style="border-radius: 5px;"/>',
                obj.imagem_principal.url
            )
        return '-'
    imagem_thumb.short_description = 'Imagem'
    
    def preco_final_display(self, obj):
        return format_html('R$ {:.2f}', obj.preco_final)
    preco_final_display.short_description = 'Preço Final'
    
    def desconto_display(self, obj):
        if obj.tem_desconto:
            return format_html(
                '<span style="color: #dc3545; font-weight: bold;">-{}%</span>',
                obj.percentual_desconto
            )
        return '-'
    desconto_display.short_description = 'Desconto'
