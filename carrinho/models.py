from django.db import models
from django.conf import settings
from produtos.models import Produto
from decimal import Decimal


class Carrinho(models.Model):
    """Carrinho de compras do usuário"""
    
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='carrinho',
        verbose_name="Usuário"
    )
    
    session_key = models.CharField(max_length=40, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Carrinho"
        verbose_name_plural = "Carrinhos"
    
    def __str__(self):
        return f"Carrinho de {self.usuario.email}"
    
    @property
    def total_itens(self):
        return sum(item.quantidade for item in self.itens.all())
    
    @property
    def subtotal(self):
        return sum(item.total for item in self.itens.all())
    
    @property
    def desconto(self):
        # Pode implementar lógica de cupons aqui
        return Decimal('0.00')
    
    @property
    def frete(self):
        # Lógica de cálculo de frete
        if self.subtotal >= 200:
            return Decimal('0.00')  # Frete grátis
        return Decimal('15.00')
    
    @property
    def total(self):
        return self.subtotal - self.desconto + self.frete


class ItemCarrinho(models.Model):
    """Item individual no carrinho"""
    
    carrinho = models.ForeignKey(
        Carrinho,
        on_delete=models.CASCADE,
        related_name='itens',
        verbose_name="Carrinho"
    )
    
    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        verbose_name="Produto"
    )
    
    quantidade = models.PositiveIntegerField(default=1, verbose_name="Quantidade")
    preco_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Preço Unitário"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Item do Carrinho"
        verbose_name_plural = "Itens do Carrinho"
        unique_together = ('carrinho', 'produto')
    
    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome}"
    
    @property
    def total(self):
        if self.preco_unitario is None:
            return Decimal('0.00')
        return self.quantidade * self.preco_unitario

    
    def save(self, *args, **kwargs):
        """Ao salvar, pega o preço do produto se não tiver"""
        if not self.preco_unitario and self.produto:
            self.preco_unitario = self.produto.preco_final
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome}"


class Pedido(models.Model):
    """Pedido finalizado"""
    
    STATUS_CHOICES = [
        ('pendente', 'Aguardando Pagamento'),
        ('pago', 'Pago'),
        ('processando', 'Em Processamento'),
        ('enviado', 'Enviado'),
        ('entregue', 'Entregue'),
        ('cancelado', 'Cancelado'),
    ]
    
    FORMA_PAGAMENTO_CHOICES = [
        ('pix', 'PIX'),
        ('cartao', 'Cartão de Crédito'),
        ('boleto', 'Boleto'),
    ]
    
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='pedidos',
        verbose_name="Usuário"
    )
    
    numero_pedido = models.CharField(max_length=20, unique=True, editable=False)
    
    # Valores
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    desconto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    frete = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Endereço de entrega
    endereco_entrega = models.TextField(verbose_name="Endereço de Entrega")
    
    # Pagamento
    forma_pagamento = models.CharField(
        max_length=20,
        choices=FORMA_PAGAMENTO_CHOICES,
        verbose_name="Forma de Pagamento"
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pendente',
        verbose_name="Status"
    )
    
    # Dados do pagamento
    payment_id = models.CharField(max_length=200, blank=True, null=True)
    qr_code_pix = models.TextField(blank=True, null=True)
    qr_code_base64 = models.TextField(blank=True, null=True)
    
    # Observações
    observacoes = models.TextField(blank=True, verbose_name="Observações")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    pago_em = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Pedido #{self.numero_pedido}"
    
    def save(self, *args, **kwargs):
        if not self.numero_pedido:
            import random
            import string
            self.numero_pedido = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        super().save(*args, **kwargs)


class ItemPedido(models.Model):
    """Item de um pedido"""
    
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name='itens',
        verbose_name="Pedido"
    )
    
    produto = models.ForeignKey(
        Produto,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Produto"
    )
    
    nome_produto = models.CharField(max_length=200)
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = "Item do Pedido"
        verbose_name_plural = "Itens do Pedido"
    
    def __str__(self):
        return f"{self.quantidade}x {self.nome_produto}"
