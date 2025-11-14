# ==========================================
# pets/admin.py - VERSÃO CORRIGIDA
# ==========================================

from django.contrib import admin
from .models import Pet, FotoPet, SolicitacaoAdocao, PromocaoAdocao


class FotoPetInline(admin.TabularInline):
    model = FotoPet
    extra = 1
    fields = ['foto', 'descricao']


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ['nome', 'especie', 'porte', 'sexo', 'idade_completa', 'status', 'created_at']
    list_filter = ['especie', 'porte', 'sexo', 'status', 'castrado', 'vacinado']
    search_fields = ['nome', 'raca', 'descricao']
    prepopulated_fields = {'slug': ('nome',)}
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'slug', 'especie', 'raca', 'porte', 'sexo')
        }),
        ('Idade e Características', {
            'fields': ('idade_anos', 'idade_meses', 'cor', 'temperamento')
        }),
        ('Descrição e Foto', {
            'fields': ('descricao', 'foto_principal')
        }),
        ('Saúde', {
            'fields': ('castrado', 'vacinado', 'vermifugado', 'necessidades_especiais')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [FotoPetInline]


@admin.register(FotoPet)
class FotoPetAdmin(admin.ModelAdmin):
    list_display = ['pet', 'descricao', 'created_at']
    list_filter = ['created_at']
    search_fields = ['pet__nome', 'descricao']


@admin.register(SolicitacaoAdocao)
class SolicitacaoAdocaoAdmin(admin.ModelAdmin):
    list_display = ['nome_completo', 'pet', 'usuario', 'status', 'created_at']
    list_filter = ['status', 'tipo_moradia', 'tem_quintal', 'created_at']
    search_fields = ['nome_completo', 'email', 'pet__nome', 'usuario__email']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Informações do Solicitante', {
            'fields': ('usuario', 'nome_completo', 'email', 'telefone', 'endereco')
        }),
        ('Pet Solicitado', {
            'fields': ('pet',)
        }),
        ('Informações da Moradia', {
            'fields': ('tipo_moradia', 'tem_quintal', 'moradia_propria')
        }),
        ('Experiência com Pets', {
            'fields': ('tem_outros_pets', 'descricao_outros_pets', 'teve_pets_antes')
        }),
        ('Motivação', {
            'fields': ('motivacao',)
        }),
        ('Status e Observações', {
            'fields': ('status', 'observacoes_admin')
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
