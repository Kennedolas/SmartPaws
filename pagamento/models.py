from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid
User = get_user_model()

class Endereco(models.Model):

    
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='enderecos'
    )
    
    nome_destinatario = models.CharField(
        max_length=100,
        verbose_name='Nome do Destinatário'
    )
    
    cep = models.CharField(max_length=9, verbose_name='CEP')
    endereco = models.CharField(max_length=200, verbose_name='Endereço')
    numero = models.CharField(max_length=20, verbose_name='Número')
    complemento = models.CharField(max_length=100, blank=True, verbose_name='Complemento')
    bairro = models.CharField(max_length=100, verbose_name='Bairro')
    cidade = models.CharField(max_length=100, verbose_name='Cidade')
    estado = models.CharField(max_length=2, verbose_name='Estado (UF)')
    
    telefone = models.CharField(
        max_length=20,
        verbose_name='Telefone para Contato'
    )
    
    principal = models.BooleanField(
        default=False,
        verbose_name='Endereço Principal?'
    )
    
    data_cadastro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'
        ordering = ['-principal', '-data_cadastro']
    
    def __str__(self):
        return f"{self.endereco}, {self.numero} - {self.cidade}/{self.estado}"
    
    def save(self, *args, **kwargs):

        if self.principal:
            Endereco.objects.filter(
                usuario=self.usuario,
                principal=True
            ).update(principal=False)
        super().save(*args, **kwargs)


class Pedido(models.Model):

    
    STATUS_PEDIDO = [
        ('pendente', 'Pendente'),
        ('aguardando_pagamento', 'Aguardando Pagamento'),
        ('pago', 'Pago'),
        ('em_separacao', 'Em Separação'),
        ('enviado', 'Enviado'),
        ('entregue', 'Entregue'),
        ('cancelado', 'Cancelado'),
        ('reembolsado', 'Reembolsado'),
    ]
    
    # Identificação
    numero_pedido = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        verbose_name='Número do Pedido'
    )
    
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    
    # Relacionamentos
    usuario = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='pedidos'
    )
    
    endereco_entrega = models.ForeignKey(
        Endereco,
        on_delete=models.PROTECT,
        related_name='pedidos'
    )
    
    # Valores
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Subtotal'
    )
    
    taxa_entrega = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name='Taxa de Entrega'
    )
    
    desconto = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name='Desconto'
    )
    
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Total'
    )
    
    # Status e datas
    status = models.CharField(
        max_length=30,
        choices=STATUS_PEDIDO,
        default='pendente'
    )
    
    data_pedido = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data do Pedido'
    )
    
    data_pagamento = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Data do Pagamento'
    )
    
    data_envio = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Data de Envio'
    )
    
    data_entrega = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Data de Entrega'
    )
    

    observacoes = models.TextField(
        blank=True,
        verbose_name='Observações'
    )
    
    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-data_pedido']
        indexes = [
            models.Index(fields=['usuario', 'status']),
            models.Index(fields=['numero_pedido']),
        ]
    
    def __str__(self):
        return f"Pedido #{self.numero_pedido} - {self.usuario.username}"
    
    def save(self, *args, **kwargs):
        if not self.numero_pedido:
            # Gerar número único do pedido
            import random
            import string
            while True:
                numero = ''.join(random.choices(string.digits, k=10))
                if not Pedido.objects.filter(numero_pedido=numero).exists():
                    self.numero_pedido = numero
                    break
        super().save(*args, **kwargs)
    
    @property
    def pode_cancelar(self):
        """Verifica se pedido pode ser cancelado"""
        return self.status in ['pendente', 'aguardando_pagamento', 'pago']
    
    @property
    def total_itens(self):
        """Total de itens no pedido"""
        return sum(item.quantidade for item in self.itens.all())


class ItemPedido(models.Model):
    """Itens do pedido"""
    
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name='itens'
    )
    
    produto = models.ForeignKey(
        'produtos.Produto',
        on_delete=models.PROTECT,
        related_name='itens_pedido'
    )
    
    loja = models.ForeignKey(
        'lojas.Loja',
        on_delete=models.PROTECT,
        related_name='itens_vendidos'
    )
    
    # Dados do produto no momento da compra
    nome_produto = models.CharField(
        max_length=200,
        verbose_name='Nome do Produto'
    )
    
    preco_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Preço Unitário'
    )
    
    quantidade = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)]
    )
    
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Subtotal'
    )
    
    class Meta:
        verbose_name = 'Item do Pedido'
        verbose_name_plural = 'Itens do Pedido'
    
    def __str__(self):
        return f"{self.quantidade}x {self.nome_produto}"
    
    def save(self, *args, **kwargs):

        self.subtotal = self.preco_unitario * self.quantidade
        super().save(*args, **kwargs)

class Pagamentos(models.Model):
    
    OPCOES_PAGAMENTO = [

        ('cartao_debito', 'Cartão de débito')
        ('cartao_credito', 'Cartão de crédito')
        ('pix', 'PIX')
        ('boleto', 'Boleto')

    ]

    STATUS_PAGAMENTO = [

        ('pendente', 'Pendente')
        ('processando', 'Processando')
        ('aprovado', 'Aprovado')
        ('cancelado', 'Cancelado')
        ('rembolsado', 'rembolsado')
    ]


    pedido = models.OneToOneField(
        Pedido,
        on_delete=models.CASCADE,
        related_name='pagamento'
    )
    
    forma_pagamento = models.CharField(
        max_length=20,
        choices=OPCOES_PAGAMENTO,
        verbose_name='Forma de Pagamento'
    )
    
    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Valor'
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_PAGAMENTO,
        default='pendente'
    )
    
    #dados do cartão
    bandeira_cartao = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Bandeira do Cartão'
    )
    
    ultimos_digitos = models.CharField(
        max_length=4,
        blank=True,
        verbose_name='Últimos 4 Dígitos'
    )
    
    # PIX
    chave_pix = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Chave PIX'
    )
    
    qr_code_pix = models.TextField(
        blank=True,
        verbose_name='QR Code PIX '
    )
    
    # Boleto
    codigo_boleto = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Código do Boleto'
    )
    
    link_boleto = models.URLField(
        blank=True,
        verbose_name='Link do Boleto'
    )
    

    transaction_id = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='ID da Transação'
    )
    
    gateway_response = models.JSONField(
        null=True,
        blank=True,
        verbose_name='Resposta do Gateway'
    )
    

    data_criacao = models.DateTimeField(auto_now_add=True)
    data_aprovacao = models.DateTimeField(null=True, blank=True)
    data_cancelamento = models.DateTimeField(null=True, blank=True)

    mensagem_erro = models.TextField(
        blank=True,
        verbose_name='Mensagem de Erro'
    )
    
    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'
        ordering = ['-data_criacao']
    
    def __str__(self):
        return f"Pagamento #{self.pedido.numero_pedido} - {self.get_forma_pagamento_display()}"


class RastreamentoEntrega(models.Model):

    
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name='rastreamentos'
    )
    
    status = models.CharField(max_length=100, verbose_name='Status')
    descricao = models.TextField(verbose_name='Descrição')
    localizacao = models.CharField(max_length=200, blank=True, verbose_name='Localização')
    data_hora = models.DateTimeField(auto_now_add=True, verbose_name='Data/Hora')
    
    class Meta:
        verbose_name = 'Rastreamento de Entrega'
        verbose_name_plural = 'Rastreamentos de Entrega'
        ordering = ['-data_hora']
    
    def __str__(self):
        return f"{self.pedido.numero_pedido} - {self.status}"