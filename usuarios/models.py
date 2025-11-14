# ==========================================
# usuarios/models.py - VERSÃO CORRIGIDA
# ==========================================

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import re
import uuid


def validar_cpf(cpf):
    """Valida CPF brasileiro"""
    cpf_numeros = re.sub(r'[^0-9]', '', str(cpf))
    
    if len(cpf_numeros) != 11:
        raise ValidationError("CPF deve ter 11 dígitos")
    
    if cpf_numeros == cpf_numeros[0] * 11:
        raise ValidationError("CPF inválido")
    
    # Validação dos dígitos verificadores
    soma = sum(int(cpf_numeros[i]) * (10 - i) for i in range(9))
    primeiro_dv = 11 - (soma % 11)
    if primeiro_dv >= 10:
        primeiro_dv = 0
    
    soma = sum(int(cpf_numeros[i]) * (11 - i) for i in range(10))
    segundo_dv = 11 - (soma % 11)
    if segundo_dv >= 10:
        segundo_dv = 0

    if primeiro_dv != int(cpf_numeros[9]) or segundo_dv != int(cpf_numeros[10]):
        raise ValidationError("CPF inválido")
    
    return cpf


class Usuario(AbstractUser):
    """Modelo customizado de usuário"""
    
    email = models.EmailField(
        unique=True,
        verbose_name="Email"
    )
    
    cpf = models.CharField(
        max_length=14,
        unique=True,
        blank=True,
        null=True,
        validators=[validar_cpf],
        verbose_name="CPF"
    )
    
    telefone_regex = RegexValidator(
        regex=r'^\(\d{2}\)\s\d{4,5}-\d{4}$',
        message="Telefone: (61) 91234-5678"
    )
    telefone = models.CharField(
        max_length=15,
        validators=[telefone_regex],
        blank=True,
        verbose_name="Telefone"
    )
    
    data_nascimento = models.DateField(
        null=True,
        blank=True,
        verbose_name="Data de Nascimento"
    )
    
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
        ('N', 'Prefiro não informar')
    ]
    sexo = models.CharField(
        max_length=1,
        choices=SEXO_CHOICES,
        blank=True,
        verbose_name="Sexo"
    )
    
    foto_perfil = models.ImageField(
        upload_to='usuarios/fotos/%Y/%m/',
        blank=True,
        null=True,
        verbose_name="Foto do Perfil"
    )
    
    is_verified = models.BooleanField(
        default=False,
        verbose_name="Email Verificado"
    )
    
    aceita_marketing = models.BooleanField(
        default=False,
        verbose_name="Aceita receber emails promocionais"
    )
    
    verification_token = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    
    reset_password_token = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # ========== CORREÇÃO DO ERRO ==========
    # Adiciona related_name para evitar conflito
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='usuario_set',  # ← ADICIONE
        related_query_name='usuario',
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='usuario_set',  # ← ADICIONE
        related_query_name='usuario',
    )
    # ========================================
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.email
    
    @property
    def nome_completo(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}".strip()
        return self.first_name or self.username
    
    @property
    def idade(self):
        if self.data_nascimento:
            from datetime import date
            today = date.today()
            return today.year - self.data_nascimento.year - (
                (today.month, today.day) < (self.data_nascimento.month, self.data_nascimento.day)
            )
        return None
    
    def generate_verification_token(self):
        self.verification_token = str(uuid.uuid4())
        self.save(update_fields=['verification_token'])
        return self.verification_token
    
    def verify_email(self):
        self.is_verified = True
        self.verification_token = None
        self.save(update_fields=['is_verified', 'verification_token'])


class Endereco(models.Model):
    """Endereços do usuário"""
    
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='enderecos',
        verbose_name="Usuário"
    )
    
    cep_regex = RegexValidator(
        regex=r'^\d{5}-?\d{3}$',
        message="CEP: 00000-000"
    )
    
    nome = models.CharField(
        max_length=100,
        verbose_name="Nome do Endereço"
    )
    
    cep = models.CharField(
        max_length=9,
        validators=[cep_regex],
        verbose_name="CEP"
    )
    
    logradouro = models.CharField(
        max_length=200,
        verbose_name="Logradouro"
    )
    
    numero = models.CharField(
        max_length=10,
        verbose_name="Número"
    )
    
    complemento = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Complemento"
    )
    
    bairro = models.CharField(
        max_length=100,
        verbose_name="Bairro"
    )
    
    cidade = models.CharField(
        max_length=100,
        verbose_name="Cidade"
    )
    
    ESTADOS_CHOICES = [
        ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'),
        ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
        ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')
    ]
    
    estado = models.CharField(
        max_length=2,
        choices=ESTADOS_CHOICES,
        verbose_name="Estado"
    )
    
    is_principal = models.BooleanField(
        default=False,
        verbose_name="Endereço Principal"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Endereço"
        verbose_name_plural = "Endereços"
        ordering = ['-is_principal', '-created_at']
    
    def __str__(self):
        return f"{self.nome} - {self.usuario.email}"
    
    @property
    def endereco_completo(self):
        endereco = f"{self.logradouro}, {self.numero}"
        if self.complemento:
            endereco += f", {self.complemento}"
        endereco += f" - {self.bairro}, {self.cidade}/{self.estado} - CEP: {self.cep}"
        return endereco
