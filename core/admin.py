from django.contrib import admin
from django.utils.html import format_html
from .models import Banner, Categoria, Beneficio, ServicoDestaque, Oferta


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['imagem_preview', 'titulo', 'ordem', 'ativo', 'created_at']
    list_editable = ['ordem', 'ativo']
    list_filter = ['ativo', 'created_at']
    search_fields = ['titulo']
    
    def imagem_preview(self, obj):
        if obj.imagem:
            return format_html(
                '<img src="{}" width="100" style="border-radius: 5px;"/>',
                obj.imagem.url
            )
        return '-'
    imagem_preview.short_description = 'Imagem'


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['imagem_preview', 'nome', 'tipo', 'ordem', 'ativo']
    list_editable = ['ordem', 'ativo']
    list_filter = ['tipo', 'ativo', 'created_at']
    search_fields = ['nome', 'slug']
    prepopulated_fields = {'slug': ('nome',)}
    
    def imagem_preview(self, obj):
        if obj.imagem:
            return format_html(
                '<img src="{}" width="60" style="border-radius: 50%;"/>',
                obj.imagem.url
            )
        return '-'
    imagem_preview.short_description = 'Imagem'


@admin.register(Beneficio)
class BeneficioAdmin(admin.ModelAdmin):
    list_display = ['icone_preview', 'titulo', 'subtitulo', 'ordem', 'ativo']
    list_editable = ['ordem', 'ativo']
    
    def icone_preview(self, obj):
        return format_html('<i class="{}"></i>', obj.icone)
    icone_preview.short_description = 'Ícone'


@admin.register(ServicoDestaque)
class ServicoDestaqueAdmin(admin.ModelAdmin):
    list_display = ['imagem_preview', 'nome', 'localizacao', 'preco_inicial', 'ordem', 'ativo']
    list_editable = ['ordem', 'ativo']
    list_filter = ['ativo', 'created_at']
    search_fields = ['nome', 'localizacao']
    
    def imagem_preview(self, obj):
        if obj.imagem:
            return format_html(
                '<img src="{}" width="80" style="border-radius: 10px;"/>',
                obj.imagem.url
            )
        return '-'
    imagem_preview.short_description = 'Imagem'


@admin.register(Oferta)
class OfertaAdmin(admin.ModelAdmin):
    list_display = ['imagem_preview', 'titulo', 'data_inicio', 'data_fim', 'ativo_badge']
    list_filter = ['ativo', 'data_inicio', 'data_fim']
    search_fields = ['titulo']
    
    def imagem_preview(self, obj):
        if obj.imagem:
            return format_html(
                '<img src="{}" width="120" style="border-radius: 10px;"/>',
                obj.imagem.url
            )
        return '-'
    imagem_preview.short_description = 'Imagem'
    
    def ativo_badge(self, obj):
        if obj.esta_ativa and obj.ativo:
            return format_html('<span style="color: #28a745;">✓ Ativa</span>')
        return format_html('<span style="color: #dc3545;">✗ Inativa</span>')
    ativo_badge.short_description = 'Status'