# ==========================================
# servicos/models.py
# ==========================================

from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator


class CategoriaServico(models.Model):
    """Categorias de serviços"""
    
    nome = models.CharField(max_length=100, verbose_name="Nome")
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    descricao = models.TextField(blank=True, verbose_name="Descrição")
    icone = models.CharField(max_length=50, blank=True, help_text="Classe do ícone FontAwesome")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    ordem = models.PositiveIntegerField(default=0, verbose_name="Ordem de Exibição")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Categoria de Serviço"
        verbose_name_plural = "Categorias de Serviços"
        ordering = ['ordem', 'nome']
    
    def __str__(self):
        return self.nome
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)


class Prestador(models.Model):
    """Prestadores de serviço"""
    
    nome = models.CharField(max_length=200, verbose_name="Nome")
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    logo = models.ImageField(upload_to='prestadores/%Y/%m/', blank=True, verbose_name="Logo")
    descricao = models.TextField(verbose_name="Descrição")
    
    # Contato
    telefone = models.CharField(max_length=20, blank=True, verbose_name="Telefone")
    whatsapp = models.CharField(max_length=20, blank=True, verbose_name="WhatsApp")
    email = models.EmailField(blank=True, verbose_name="Email")
    site = models.URLField(blank=True, verbose_name="Site")
    
    # Endereço
    endereco = models.CharField(max_length=300, verbose_name="Endereço")
    bairro = models.CharField(max_length=100, verbose_name="Bairro")
    cidade = models.CharField(max_length=100, verbose_name="Cidade")
    estado = models.CharField(max_length=2, verbose_name="Estado")
    cep = models.CharField(max_length=9, blank=True, verbose_name="CEP")
    
    # Avaliação
    avaliacao_media = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name="Avaliação Média"
    )
    total_avaliacoes = models.PositiveIntegerField(default=0, verbose_name="Total de Avaliações")
    
    # Controle
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    destaque = models.BooleanField(default=False, verbose_name="Destaque")
    verificado = models.BooleanField(default=False, verbose_name="Verificado")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Prestador"
        verbose_name_plural = "Prestadores"
        ordering = ['-destaque', '-avaliacao_media', 'nome']
    
    def __str__(self):
        return self.nome
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)
    
    @property
    def endereco_completo(self):
        return f"{self.endereco}, {self.bairro} - {self.cidade}/{self.estado}"


class Servico(models.Model):
    """Serviços oferecidos"""
    
    UNIDADE_TEMPO_CHOICES = [
        ('hora', 'Por hora'),
        ('dia', 'Por dia'),
        ('semana', 'Por semana'),
        ('mes', 'Por mês'),
        ('servico', 'Por serviço'),
    ]
    
    prestador = models.ForeignKey(
        Prestador,
        on_delete=models.CASCADE,
        related_name='servicos',
        verbose_name="Prestador"
    )
    
    categoria = models.ForeignKey(
        CategoriaServico,
        on_delete=models.SET_NULL,
        null=True,
        related_name='servicos',
        verbose_name="Categoria"
    )
    
    nome = models.CharField(max_length=200, verbose_name="Nome do Serviço")
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    descricao = models.TextField(verbose_name="Descrição")
    descricao_curta = models.CharField(max_length=200, blank=True, verbose_name="Descrição Curta")
    
    # Preço
    preco = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name="Preço"
    )
    unidade_tempo = models.CharField(
        max_length=20,
        choices=UNIDADE_TEMPO_CHOICES,
        default='servico',
        verbose_name="Unidade de Tempo"
    )
    
    # Detalhes
    duracao = models.CharField(max_length=100, blank=True, verbose_name="Duração Estimada")
    inclui = models.TextField(blank=True, verbose_name="O que está incluído")
    requisitos = models.TextField(blank=True, verbose_name="Requisitos")
    
    # Imagens
    imagem_principal = models.ImageField(
        upload_to='servicos/%Y/%m/',
        verbose_name="Imagem Principal"
    )
    
    # Controle
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    destaque = models.BooleanField(default=False, verbose_name="Destaque")
    disponibilidade = models.CharField(max_length=200, blank=True, verbose_name="Disponibilidade")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Serviço"
        verbose_name_plural = "Serviços"
        ordering = ['-destaque', '-created_at']
    
    def __str__(self):
        return f"{self.nome} - {self.prestador.nome}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.nome}-{self.prestador.nome}")
            self.slug = base_slug
        super().save(*args, **kwargs)
    
    @property
    def preco_formatado(self):
        return f"R$ {self.preco:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


class AgendamentoServico(models.Model):
    """Agendamentos de serviços"""
    
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('confirmado', 'Confirmado'),
        ('em_andamento', 'Em Andamento'),
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado'),
    ]
    
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='agendamentos',
        verbose_name="Usuário"
    )
    
    servico = models.ForeignKey(
        Servico,
        on_delete=models.CASCADE,
        related_name='agendamentos',
        verbose_name="Serviço"
    )
    
    # Dados do agendamento
    data_agendamento = models.DateField(verbose_name="Data do Agendamento")
    horario = models.TimeField(verbose_name="Horário")
    
    # Dados do cliente
    nome_pet = models.CharField(max_length=100, verbose_name="Nome do Pet")
    observacoes = models.TextField(blank=True, verbose_name="Observações")
    
    # Controle
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pendente',
        verbose_name="Status"
    )
    
    observacoes_prestador = models.TextField(blank=True, verbose_name="Observações do Prestador")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Agendamento"
        verbose_name_plural = "Agendamentos"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.servico.nome} - {self.usuario.email} - {self.data_agendamento}"
