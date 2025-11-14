# ==========================================
# servicos/admin.py
# ==========================================

from django.contrib import admin
from .models import CategoriaServico, Prestador, Servico, AgendamentoServico


@admin.register(CategoriaServico)
class CategoriaServicoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'slug', 'ativo', 'ordem']
    list_filter = ['ativo']
    search_fields = ['nome']
    prepopulated_fields = {'slug': ('nome',)}


@admin.register(Prestador)
class PrestadorAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cidade', 'estado', 'avaliacao_media', 'verificado', 'ativo']
    list_filter = ['ativo', 'verificado', 'destaque', 'cidade', 'estado']
    search_fields = ['nome', 'cidade']
    prepopulated_fields = {'slug': ('nome',)}


@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'prestador', 'categoria', 'preco', 'ativo', 'destaque']
    list_filter = ['ativo', 'destaque', 'categoria', 'unidade_tempo']
    search_fields = ['nome', 'prestador__nome']
    prepopulated_fields = {'slug': ('nome',)}


@admin.register(AgendamentoServico)
class AgendamentoServicoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'servico', 'data_agendamento', 'horario', 'status', 'created_at']
    list_filter = ['status', 'data_agendamento', 'created_at']
    search_fields = ['usuario__email', 'servico__nome', 'nome_pet']
    readonly_fields = ['created_at', 'updated_at']
