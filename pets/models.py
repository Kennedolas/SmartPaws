# ==========================================
# pets/models.py - VERSÃO CORRIGIDA
# ==========================================

from django.db import models
from django.conf import settings  # ← IMPORTE settings
from django.utils.text import slugify


class Pet(models.Model):
    """Modelo de Pet para adoção"""
    
    ESPECIE_CHOICES = [
        ('cao', 'Cão'),
        ('gato', 'Gato'),
        ('ave', 'Ave'),
        ('roedor', 'Roedor'),
        ('reptil', 'Réptil'),
        ('outro', 'Outro'),
    ]
    
    PORTE_CHOICES = [
        ('mini', 'Mini'),
        ('pequeno', 'Pequeno'),
        ('medio', 'Médio'),
        ('grande', 'Grande'),
        ('gigante', 'Gigante'),
    ]
    
    SEXO_CHOICES = [
        ('M', 'Macho'),
        ('F', 'Fêmea'),
    ]
    
    STATUS_CHOICES = [
        ('disponivel', 'Disponível'),
        ('adotado', 'Adotado'),
        ('processo', 'Em Processo de Adoção'),
    ]
    
    nome = models.CharField(max_length=100, verbose_name="Nome do Pet")
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    especie = models.CharField(max_length=20, choices=ESPECIE_CHOICES, verbose_name="Espécie")
    raca = models.CharField(max_length=100, blank=True, verbose_name="Raça")
    porte = models.CharField(max_length=20, choices=PORTE_CHOICES, verbose_name="Porte")
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, verbose_name="Sexo")
    idade_anos = models.PositiveIntegerField(default=0, verbose_name="Idade (anos)")
    idade_meses = models.PositiveIntegerField(default=0, verbose_name="Idade (meses)")
    cor = models.CharField(max_length=50, blank=True, verbose_name="Cor")
    descricao = models.TextField(verbose_name="Descrição")
    temperamento = models.CharField(max_length=200, blank=True, verbose_name="Temperamento")
    foto_principal = models.ImageField(upload_to='pets/%Y/%m/', verbose_name="Foto Principal")
    castrado = models.BooleanField(default=False, verbose_name="Castrado")
    vacinado = models.BooleanField(default=False, verbose_name="Vacinado")
    vermifugado = models.BooleanField(default=False, verbose_name="Vermifugado")
    necessidades_especiais = models.TextField(blank=True, verbose_name="Necessidades Especiais")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='disponivel', verbose_name="Status")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Pet"
        verbose_name_plural = "Pets"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.nome} - {self.get_especie_display()}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)
    
    @property
    def idade_completa(self):
        if self.idade_anos > 0 and self.idade_meses > 0:
            return f"{self.idade_anos} ano(s) e {self.idade_meses} mês(es)"
        elif self.idade_anos > 0:
            return f"{self.idade_anos} ano(s)"
        else:
            return f"{self.idade_meses} mês(es)"


class FotoPet(models.Model):
    """Fotos adicionais do pet"""
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='fotos_adicionais')
    foto = models.ImageField(upload_to='pets/%Y/%m/')
    descricao = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Foto do Pet"
        verbose_name_plural = "Fotos dos Pets"
    
    def __str__(self):
        return f"Foto de {self.pet.nome}"


class SolicitacaoAdocao(models.Model):
    """Solicitações de adoção"""
    
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('analise', 'Em Análise'),
        ('aprovada', 'Aprovada'),
        ('recusada', 'Recusada'),
    ]
    
    # ========== CORREÇÃO DO ERRO ==========
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # ← MUDANÇA AQUI
        on_delete=models.CASCADE,
        related_name='solicitacoes_adocao',
        verbose_name="Usuário"
    )
    # ======================================
    
    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name='solicitacoes',
        verbose_name="Pet"
    )
    
    nome_completo = models.CharField(max_length=200, verbose_name="Nome Completo")
    email = models.EmailField(verbose_name="Email")
    telefone = models.CharField(max_length=20, verbose_name="Telefone")
    endereco = models.TextField(verbose_name="Endereço")
    
    # Informações sobre moradia
    tipo_moradia = models.CharField(
        max_length=50,
        choices=[
            ('casa', 'Casa'),
            ('apartamento', 'Apartamento'),
            ('sitio', 'Sítio/Chácara'),
        ],
        verbose_name="Tipo de Moradia"
    )
    tem_quintal = models.BooleanField(default=False, verbose_name="Tem Quintal")
    moradia_propria = models.BooleanField(default=False, verbose_name="Moradia Própria")
    
    # Experiência com pets
    tem_outros_pets = models.BooleanField(default=False, verbose_name="Tem Outros Pets")
    descricao_outros_pets = models.TextField(blank=True, verbose_name="Descrição dos Outros Pets")
    teve_pets_antes = models.BooleanField(default=False, verbose_name="Já Teve Pets Antes")
    
    # Motivação
    motivacao = models.TextField(verbose_name="Por que deseja adotar?")
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pendente',
        verbose_name="Status"
    )
    
    observacoes_admin = models.TextField(blank=True, verbose_name="Observações da Administração")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Solicitação de Adoção"
        verbose_name_plural = "Solicitações de Adoção"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Solicitação de {self.nome_completo} para {self.pet.nome}"


class PromocaoAdocao(models.Model):
    """Promoções especiais de adoção"""
    
    titulo = models.CharField(max_length=200, verbose_name="Título")
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    descricao = models.TextField(verbose_name="Descrição")
    banner = models.ImageField(upload_to='promocoes/%Y/%m/', verbose_name="Banner")
    data_inicio = models.DateField(verbose_name="Data de Início")
    data_fim = models.DateField(verbose_name="Data de Término")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    
    # ========== CORREÇÃO DO ERRO ==========
    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,  
        on_delete=models.SET_NULL,
        null=True,
        related_name='promocoes_criadas',
        verbose_name="Criado Por"
    )
    # ======================================
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Promoção de Adoção"
        verbose_name_plural = "Promoções de Adoção"
        ordering = ['-data_inicio']
    
    def __str__(self):
        return self.titulo
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)
