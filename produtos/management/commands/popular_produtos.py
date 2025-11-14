# produtos/management/commands/popular_produtos.py

from django.core.management.base import BaseCommand
from produtos.models import CategoriaProduto, Produto
from decimal import Decimal


class Command(BaseCommand):
    help = 'Popula o banco de dados com produtos de exemplo'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('🚀 Iniciando população do banco...\n'))
        
        # ========== CRIAR CATEGORIAS ==========
        self.stdout.write('📂 Criando categorias...')
        
        categorias_data = [
            {'nome': 'Alimentos', 'tipo': 'alimentos', 'slug': 'alimentos'},
            {'nome': 'Brinquedos', 'tipo': 'brinquedos', 'slug': 'brinquedos'},
            {'nome': 'Roupas e Acessórios', 'tipo': 'roupas_acessorios', 'slug': 'roupas-acessorios'},
        ]
        
        categorias = {}
        for cat_data in categorias_data:
            categoria, created = CategoriaProduto.objects.get_or_create(
                nome=cat_data['nome'],
                defaults={
                    'tipo': cat_data['tipo'],
                    'slug': cat_data['slug'],
                    'ativo': True
                }
            )
            categorias[cat_data['nome']] = categoria
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✅ Criada: {categoria.nome}'))
            else:
                self.stdout.write(self.style.WARNING(f'  ⚠️  Já existe: {categoria.nome}'))
        
        # ========== CRIAR PRODUTOS ==========
        self.stdout.write('\n🛍️  Criando produtos...')
        
        produtos_data = [
            {
                'nome': 'Ração para Cães Sabor Carne SmartPaws',
                'categoria': categorias['Alimentos'],
                'descricao': 'Ração premium para cães adultos.',
                'preco_original': Decimal('999.99'),
                'preco_desconto': Decimal('9.99'),
                'estoque': 100,
                'avaliacao': Decimal('5.0'),
                'peso_tamanho': '15kg',
                'ativo': True,
                'destaque': True,
            },
            {
                'nome': 'Ração Úmida para Gatos Sabor Salmão',
                'categoria': categorias['Alimentos'],
                'descricao': 'Deliciosa ração úmida com salmão.',
                'preco_original': Decimal('999.99'),
                'preco_desconto': Decimal('9.99'),
                'estoque': 150,
                'avaliacao': Decimal('5.0'),
                'peso_tamanho': '150g',
                'ativo': True,
            },
            {
                'nome': 'Brinquedo de Pelúcia Osso',
                'categoria': categorias['Brinquedos'],
                'descricao': 'Brinquedo macio para cães.',
                'preco_original': Decimal('999.99'),
                'preco_desconto': Decimal('9.99'),
                'estoque': 80,
                'avaliacao': Decimal('5.0'),
                'ativo': True,
            },
            {
                'nome': 'Conjunto Moletom Azul para Cachorros',
                'categoria': categorias['Roupas e Acessórios'],
                'descricao': 'Moletom confortável para cães.',
                'preco_original': Decimal('999.99'),
                'preco_desconto': Decimal('9.99'),
                'estoque': 60,
                'avaliacao': Decimal('5.0'),
                'ativo': True,
            },
            {
                'nome': 'Pijama Poliéster para Cães',
                'categoria': categorias['Roupas e Acessórios'],
                'descricao': 'Pijama quentinho para pets.',
                'preco_original': Decimal('999.99'),
                'preco_desconto': Decimal('9.99'),
                'estoque': 45,
                'avaliacao': Decimal('5.0'),
                'ativo': True,
            },
        ]
        
        for produto_data in produtos_data:
            produto, created = Produto.objects.get_or_create(
                nome=produto_data['nome'],
                defaults=produto_data
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✅ Criado: {produto.nome}'))
            else:
                self.stdout.write(self.style.WARNING(f'  ⚠️  Já existe: {produto.nome}'))
        
        self.stdout.write(self.style.SUCCESS('\n🎉 Banco populado com sucesso!'))
        self.stdout.write(self.style.SUCCESS(f'Total: {Produto.objects.count()} produtos'))
