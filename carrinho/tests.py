from django.test import TestCase
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from decimal import Decimal

from .models import Carrinho, ItemCarrinho
from produtos.models import Produto, Categoria, Marca

User = get_user_model()


class CarrinhoTestCase(TestCase):
    
    def setUp(self):
        # Criar usuário
        self.user = User.objects.create_user(
            username='test',
            email='test@test.com',
            password='test123'
        )
        
        # Criar categoria e marca
        self.categoria = Categoria.objects.create(
            nome='Ração',
            ativo=True
        )
        
        self.marca = Marca.objects.create(
            nome='Test Brand',
            ativo=True
        )
        
        # Criar produto
        self.produto = Produto.objects.create(
            nome='Ração Test',
            categoria=self.categoria,
            marca=self.marca,
            preco=Decimal('50.00'),
            estoque=10,
            ativo=True
        )
        
        # Criar carrinho
        self.carrinho = Carrinho.objects.create(usuario=self.user)
    
    def test_adicionar_produto_ao_carrinho(self):

        item = self.carrinho.adicionar_produto(self.produto, 2)
        
        self.assertEqual(item.quantidade, 2)
        self.assertEqual(item.produto, self.produto)
        self.assertEqual(self.carrinho.total_itens, 2)
    
    def test_adicionar_produto_existente(self):

        self.carrinho.adicionar_produto(self.produto, 1)
        
        # Adicionar novamente
        self.carrinho.adicionar_produto(self.produto, 2)
        
        # Deve ter apenas 1 item com quantidade 3
        self.assertEqual(self.carrinho.itens.count(), 1)
        self.assertEqual(self.carrinho.total_itens, 3)
    
    def test_validacao_estoque(self):
        """Testa validação de estoque"""
        with self.assertRaises(ValidationError):
            self.carrinho.adicionar_produto(self.produto, 15)  # Mais que estoque
    
    def test_calculos_carrinho(self):
        """Testa cálculos do carrinho"""
        self.carrinho.adicionar_produto(self.produto, 2)
        
        self.assertEqual(self.carrinho.subtotal, Decimal('100.00'))
        self.assertEqual(self.carrinho.total_preco, Decimal('100.00'))
    
    def test_remover_produto(self):
        """Testa remover produto do carrinho"""
        self.carrinho.adicionar_produto(self.produto, 1)
        
        resultado = self.carrinho.remover_produto(self.produto)
        
        self.assertTrue(resultado)
        self.assertEqual(self.carrinho.total_itens, 0)
    
    def test_limpar_carrinho(self):
        """Testa limpar carrinho"""
        self.carrinho.adicionar_produto(self.produto, 2)
        
        self.carrinho.limpar()
        
        self.assertTrue(self.carrinho.esta_vazio)
        self.assertEqual(self.carrinho.total_itens, 0)

