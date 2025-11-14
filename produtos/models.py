

from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal


class CategoriaProduto(models.Model):
    """Categorias de produtos"""
    
    TIPO_CHOICES = [
        ('alimentos', 'Alimentos'),
        ('brinquedos', 'Brinquedos'),
        ('gaiolas_viveiros', 'Gaiolas e Viveiros'),
        ('roupas_acessorios', 'Roupas e Acessórios'),
        ('higiene', 'Higiene'),
        ('outros', 'Outros'),
    ]
    
    nome = models.CharField(
        max_length=100,
        verbose_name="Nome da Categoria"
    )
    
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name="URL Amigável"
    )
    
    tipo = models.CharField(
        max_length=30,
        choices=TIPO_CHOICES,
        verbose_name="Tipo"
    )
    
    descricao = models.TextField(
        blank=True,
        verbose_name="Descrição"
    )
    
    imagem = models.ImageField(
        upload_to='categorias/%Y/%m/',
        null=True,
        blank=True,
        verbose_name="Imagem"
    )
    
    ordem = models.PositiveIntegerField(
        default=0,
        verbose_name="Ordem de Exibição"
    )
    
    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativo"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Categoria de Produto"
        verbose_name_plural = "Categorias de Produtos"
        ordering = ['ordem', 'nome']
    
    def __str__(self):
        return self.nome
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)


class Produto(models.Model):
    """Produtos da loja"""
    
    # Informações básicas
    nome = models.CharField(
        max_length=200,
        verbose_name="Nome do Produto"
    )
    
    slug = models.SlugField(
        max_length=200,
        unique=True,
        blank=True,
        verbose_name="URL Amigável"
    )
    
    categoria = models.ForeignKey(
        CategoriaProduto,
        on_delete=models.PROTECT,
        related_name='produtos',
        verbose_name="Categoria"
    )
    
    descricao = models.TextField(
        verbose_name="Descrição"
    )
    
    # Imagens
    imagem_principal = models.ImageField(
        upload_to='produtos/%Y/%m/',
        verbose_name="Imagem Principal"
    )
    
    # Preços
    preco_original = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Preço Original (R$)"
    )
    
    preco_desconto = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Preço com Desconto (R$)"
    )
    
    # Estoque
    estoque = models.PositiveIntegerField(
        default=0,
        verbose_name="Quantidade em Estoque"
    )
    
    estoque_minimo = models.PositiveIntegerField(
        default=5,
        verbose_name="Estoque Mínimo"
    )
    
    # Avaliação
    avaliacao = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=Decimal('5.0'),
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name="Avaliação (0-5)"
    )
    
    numero_avaliacoes = models.PositiveIntegerField(
        default=0,
        verbose_name="Número de Avaliações"
    )
    
    # Características
    peso_tamanho = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Peso/Tamanho"
    )
    
    marca = models.CharField(
        max_length=100,
        default="SmartPaws",
        verbose_name="Marca"
    )
    
    # Destaque
    destaque = models.BooleanField(
        default=False,
        verbose_name="Produto em Destaque"
    )
    
    novidade = models.BooleanField(
        default=False,
        verbose_name="Novidade"
    )
    
    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativo"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['categoria', 'ativo']),
        ]
    
    def __str__(self):
        return self.nome
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)
    
    @property
    def preco_final(self):
        """Retorna o preço final (com ou sem desconto)"""
        return self.preco_desconto if self.preco_desconto else self.preco_original
    
    @property
    def percentual_desconto(self):
        """Calcula percentual de desconto"""
        if self.preco_desconto and self.preco_desconto < self.preco_original:
            desconto = ((self.preco_original - self.preco_desconto) / self.preco_original) * 100
            return int(desconto)
        return 0
    
    @property
    def tem_desconto(self):
        """Verifica se produto tem desconto"""
        return self.preco_desconto and self.preco_desconto < self.preco_original
    
    @property
    def em_estoque(self):
        """Verifica se tem estoque"""
        return self.estoque > 0
    
    @property
    def estoque_baixo(self):
        """Verifica se estoque está baixo"""
        return 0 < self.estoque <= self.estoque_minimo


class ImagemProduto(models.Model):
    """Imagens adicionais do produto"""
    
    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        related_name='imagens_adicionais',
        verbose_name="Produto"
    )
    
    imagem = models.ImageField(
        upload_to='produtos/galeria/%Y/%m/',
        verbose_name="Imagem"
    )
    
    ordem = models.PositiveIntegerField(
        default=0,
        verbose_name="Ordem"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Imagem do Produto"
        verbose_name_plural = "Imagens dos Produtos"
        ordering = ['ordem']
    
    def __str__(self):
        return f"Imagem {self.ordem} - {self.produto.nome}"
