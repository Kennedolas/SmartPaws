# ==========================================
# usuarios/admin.py
# ==========================================

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Endereco


class EnderecoInline(admin.TabularInline):
    model = Endereco
    extra = 0
    fields = ['nome', 'cep', 'logradouro', 'numero', 'bairro', 'cidade', 'estado', 'is_principal']


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ['email', 'nome_completo', 'cpf', 'is_verified', 'is_staff', 'created_at']
    list_filter = ['is_verified', 'is_staff', 'is_active', 'sexo', 'created_at']
    search_fields = ['email', 'first_name', 'last_name', 'cpf']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Informações de Login', {
            'fields': ('email', 'username', 'password')
        }),
        ('Informações Pessoais', {
            'fields': ('first_name', 'last_name', 'cpf', 'telefone', 'data_nascimento', 'sexo', 'foto_perfil')
        }),
        ('Verificação', {
            'fields': ('is_verified', 'verification_token')
        }),
        ('Permissões', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Datas Importantes', {
            'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at', 'last_login', 'date_joined']
    
    inlines = [EnderecoInline]
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )


@admin.register(Endereco)
class EnderecoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'nome', 'cidade', 'estado', 'is_principal', 'created_at']
    list_filter = ['estado', 'is_principal', 'created_at']
    search_fields = ['usuario__email', 'logradouro', 'cidade', 'bairro']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Usuário', {
            'fields': ('usuario',)
        }),
        ('Identificação', {
            'fields': ('nome', 'is_principal')
        }),
        ('Endereço', {
            'fields': ('cep', 'logradouro', 'numero', 'complemento', 'bairro', 'cidade', 'estado')
        }),
    )
