from django.db import models
from django.utils import timezone


class Banner(models.Model):
    """Banners rotativos da página inicial"""
    
    titulo = models.CharField(
        max_length=200,
        verbose_name="Título"
    )
    
    imagem = models.ImageField(
        upload_to='banners/%Y/%m/',
        verbose_name="Imagem do Banner"
    )
    
    link = models.URLField(
        blank=True,
        verbose_name="Link (opcional)"
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
    
    class Meta:
        verbose_name = "Banner"
        verbose_name_plural = "Banners"
        ordering = ['ordem', '-created_at']
    
    def __str__(self):
        return self.titulo


class Categoria(models.Model):
    """Categorias de produtos (Mais Procurados)"""
    
    TIPO_CHOICES = [
        ('mais_procurado', 'Mais Procurado'),
        ('especie', 'Categoria por Espécie'),
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
    
    imagem = models.ImageField(
        upload_to='categorias/%Y/%m/',
        verbose_name="Imagem"
    )
    
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        default='mais_procurado',
        verbose_name="Tipo"
    )
    
    descricao = models.TextField(
        blank=True,
        verbose_name="Descrição"
    )
    
    ordem = models.PositiveIntegerField(
        default=0,
        verbose_name="Ordem"
    )
    
    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativo"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['ordem', 'nome']
    
    def __str__(self):
        return self.nome


class Beneficio(models.Model):
    """Benefícios exibidos na home (Entrega Expressa, Frete Grátis, etc)"""
    
    icone = models.CharField(
        max_length=50,
        default='fas fa-truck',
        help_text='Classe do ícone FontAwesome',
        verbose_name="Ícone"
    )
    
    titulo = models.CharField(
        max_length=100,
        verbose_name="Título Principal"
    )
    
    subtitulo = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Subtítulo"
    )
    
    ordem = models.PositiveIntegerField(
        default=0,
        verbose_name="Ordem"
    )
    
    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativo"
    )
    
    class Meta:
        verbose_name = "Benefício"
        verbose_name_plural = "Benefícios"
        ordering = ['ordem']
    
    def __str__(self):
        return self.titulo


class ServicoDestaque(models.Model):
    """Serviços em destaque na home"""
    
    nome = models.CharField(
        max_length=200,
        verbose_name="Nome do Serviço"
    )
    
    imagem = models.ImageField(
        upload_to='servicos_destaque/%Y/%m/',
        verbose_name="Imagem do Local"
    )
    
    avaliacao = models.ImageField(
        upload_to='avaliacoes/',
        verbose_name="Imagem de Avaliação"
    )
    
    localizacao = models.CharField(
        max_length=200,
        verbose_name="Localização"
    )
    
    descricao = models.TextField(
        verbose_name="Descrição"
    )
    
    preco_inicial = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Preço Inicial (R$)"
    )
    
    link = models.URLField(
        blank=True,
        verbose_name="Link para o Serviço"
    )
    
    ordem = models.PositiveIntegerField(
        default=0,
        verbose_name="Ordem"
    )
    
    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativo"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Serviço em Destaque"
        verbose_name_plural = "Serviços em Destaque"
        ordering = ['ordem', '-created_at']
    
    def __str__(self):
        return self.nome


class Oferta(models.Model):
    """Ofertas especiais (banner grande)"""
    
    titulo = models.CharField(
        max_length=200,
        verbose_name="Título"
    )
    
    imagem = models.ImageField(
        upload_to='ofertas/%Y/%m/',
        verbose_name="Imagem da Oferta"
    )
    
    link = models.URLField(
        blank=True,
        verbose_name="Link"
    )
    
    data_inicio = models.DateTimeField(
        default=timezone.now,
        verbose_name="Início da Oferta"
    )
    
    data_fim = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fim da Oferta"
    )
    
    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativo"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Oferta"
        verbose_name_plural = "Ofertas"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.titulo
    
    @property
    def esta_ativa(self):
        """Verifica se oferta está dentro do período"""
        agora = timezone.now()
        if self.data_fim:
            return self.data_inicio <= agora <= self.data_fim
        return self.data_inicio <= agora
