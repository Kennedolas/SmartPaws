# ==========================================
# apps/produtos/tests.py
# ==========================================

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from decimal import Decimal
import json
import tempfile
from PIL import Image
import io

from .models import Categoria, Marca, Produto, ImagemProduto, Avaliacao, Lista
from .forms import ProdutoFilterForm, AvaliacaoForm, BuscaForm, AdicionarCarrinhoForm
#from apps.carrinho.models import Carrinho, ItemCarrinho

User = get_user_model()


class ProdutoTestCase(TestCase):
    """Testes base com dados compartilhados"""
    
    @classmethod
    def setUpTestData(cls):
        """Configuração executada uma vez para toda a classe"""
        # Usuário para testes
        cls.user = User.objects.create_user(
            username='testuser',
            email='test@petshop.com',
            password='testpass123'
        )
        
        # Categoria
        cls.categoria = Categoria.objects.create(
            nome='Ração para Cães',
            slug='racao-caes',
            descricao='Ração nutritiva para cães',
            ativo=True
        )
        
        # Marca
        cls.marca = Marca.objects.create(
            nome='Pedigree',
            slug='pedigree',
            descricao='Marca premium para pets',
            ativo=True
        )
        
        # Produto
        cls.produto = Produto.objects.create(
            nome='Ração Pedigree Adulto',
            slug='racao-pedigree-adulto',
            descricao='Ração completa para cães adultos',
            categoria=cls.categoria,
            marca=cls.marca,
            preco=Decimal('49.90'),
            estoque=100,
            ativo=True,
            tipo_animal='cao',
            idade_animal='adulto'
        )
    
    def setUp(self):
        """Configuração executada antes de cada teste"""
        self.client = Client()


class CategoriaModelTest(ProdutoTestCase):
    """Testes para o modelo Categoria"""
    
    def test_categoria_creation(self):
        """Testa criação de categoria"""
        categoria = Categoria.objects.create(
            nome='Brinquedos',
            descricao='Brinquedos para pets'
        )
        
        self.assertEqual(categoria.nome, 'Brinquedos')
        self.assertEqual(categoria.slug, 'brinquedos')  # Auto gerado
        self.assertTrue(categoria.ativo)
        self.assertEqual(categoria.ordem, 0)
    
    def test_categoria_str_method(self):
        """Testa método __str__"""
        self.assertEqual(str(self.categoria), 'Ração para Cães')
    
    def test_categoria_absolute_url(self):
        """Testa get_absolute_url"""
        expected_url = reverse('produtos:categoria', kwargs={'slug': self.categoria.slug})
        self.assertEqual(self.categoria.get_absolute_url(), expected_url)
    
    def test_categoria_slug_unique(self):
        """Testa unicidade do slug"""
        with self.assertRaises(IntegrityError):
            Categoria.objects.create(
                nome='Ração para Cães',  # Nome diferente
                slug='racao-caes'        # Mas slug igual
            )
    
    def test_categoria_slug_auto_generation(self):
        """Testa geração automática de slug único"""
        # Criar categoria com nome similar
        categoria2 = Categoria.objects.create(nome='Ração para Cães Premium')
        self.assertEqual(categoria2.slug, 'racao-para-caes-premium')
        
        # Criar outra com nome que geraria slug duplicado
        categoria3 = Categoria.objects.create(nome='Ração Para Cães')  # Capitalização diferente
        self.assertEqual(categoria3.slug, 'racao-para-caes-1')  # Numerado automaticamente
    
    def test_total_produtos_property(self):
        """Testa propriedade total_produtos"""
        self.assertEqual(self.categoria.total_produtos, 1)  # Um produto criado no setUp
        
        # Criar produto inativo - não deve contar
        Produto.objects.create(
            nome='Produto Inativo',
            categoria=self.categoria,
            marca=self.marca,
            preco=Decimal('10.00'),
            ativo=False
        )
        
        self.assertEqual(self.categoria.total_produtos, 1)  # Ainda deve ser 1


class MarcaModelTest(ProdutoTestCase):
    """Testes para o modelo Marca"""
    
    def test_marca_creation(self):
        """Testa criação de marca"""
        marca = Marca.objects.create(
            nome='Royal Canin',
            descricao='Nutrição científica para pets',
            pais_origem='França'
        )
        
        self.assertEqual(marca.nome, 'Royal Canin')
        self.assertEqual(marca.slug, 'royal-canin')
        self.assertEqual(marca.pais_origem, 'França')
        self.assertTrue(marca.ativo)
    
    def test_marca_str_method(self):
        """Testa método __str__"""
        self.assertEqual(str(self.marca), 'Pedigree')
    
    def test_total_produtos_property(self):
        """Testa propriedade total_produtos"""
        self.assertEqual(self.marca.total_produtos, 1)


class ProdutoModelTest(ProdutoTestCase):
    """Testes para o modelo Produto"""
    
    def test_produto_creation(self):
        """Testa criação de produto"""
        produto = Produto.objects.create(
            nome='Ração Super Premium',
            categoria=self.categoria,
            marca=self.marca,
            preco=Decimal('89.90'),
            preco_promocional=Decimal('79.90'),
            estoque=50,
            peso=Decimal('15.000'),
            tipo_animal='gato',
            idade_animal='filhote'
        )
        
        self.assertEqual(produto.nome, 'Ração Super Premium')
        self.assertEqual(produto.slug, 'racao-super-premium')
        self.assertTrue(produto.sku.startswith('PROD-'))  # Auto gerado
        self.assertEqual(len(produto.sku), 13)  # PROD- + 8 caracteres
    
    def test_produto_str_method(self):
        """Testa método __str__"""
        self.assertEqual(str(self.produto), 'Ração Pedigree Adulto')
    
    def test_produto_absolute_url(self):
        """Testa get_absolute_url"""
        expected_url = reverse('produtos:detalhe', kwargs={'slug': self.produto.slug})
        self.assertEqual(self.produto.get_absolute_url(), expected_url)
    
    def test_preco_final_property(self):
        """Testa propriedade preco_final"""
        # Sem promoção
        self.assertEqual(self.produto.preco_final, Decimal('49.90'))
        
        # Com promoção
        self.produto.preco_promocional = Decimal('39.90')
        self.produto.save()
        self.assertEqual(self.produto.preco_final, Decimal('39.90'))
    
    def test_tem_desconto_property(self):
        """Testa propriedade tem_desconto"""
        # Sem desconto
        self.assertFalse(self.produto.tem_desconto)
        
        # Com desconto
        self.produto.preco_promocional = Decimal('39.90')
        self.produto.save()
        self.assertTrue(self.produto.tem_desconto)
        
        # Preço promocional maior (não deveria acontecer, mas testa)
        self.produto.preco_promocional = Decimal('59.90')
        self.produto.save()
        self.assertFalse(self.produto.tem_desconto)
    
    def test_percentual_desconto_property(self):
        """Testa cálculo de percentual de desconto"""
        # Sem desconto
        self.assertEqual(self.produto.percentual_desconto, 0)
        
        # Com 20% de desconto (49.90 -> 39.92)
        self.produto.preco_promocional = Decimal('39.92')
        self.produto.save()
        self.assertEqual(self.produto.percentual_desconto, 20)
    
    def test_estoque_baixo_property(self):
        """Testa propriedade estoque_baixo"""
        # Estoque alto
        self.assertFalse(self.produto.estoque_baixo)
        
        # Estoque baixo
        self.produto.estoque = 3  # Menor que estoque_minimo (5)
        self.produto.save()
        self.assertTrue(self.produto.estoque_baixo)
        
        # Sem controle de estoque
        self.produto.controlar_estoque = False
        self.produto.save()
        self.assertFalse(self.produto.estoque_baixo)
    
    def test_disponivel_property(self):
        """Testa propriedade disponivel"""
        # Produto ativo com estoque
        self.assertTrue(self.produto.disponivel)
        
        # Produto inativo
        self.produto.ativo = False
        self.produto.save()
        self.assertFalse(self.produto.disponivel)
        
        # Produto ativo sem estoque
        self.produto.ativo = True
        self.produto.estoque = 0
        self.produto.save()
        self.assertFalse(self.produto.disponivel)
        
        # Produto ativo sem controle de estoque
        self.produto.controlar_estoque = False
        self.produto.save()
        self.assertTrue(self.produto.disponivel)
    
    def test_margem_lucro_property(self):
        """Testa cálculo de margem de lucro"""
        # Sem preço de custo
        self.assertEqual(self.produto.margem_lucro, 0)
        
        # Com preço de custo (49.90 venda, 30.00 custo = 66.33% margem)
        self.produto.preco_custo = Decimal('30.00')
        self.produto.save()
        self.assertAlmostEqual(self.produto.margem_lucro, 66.33, places=1)
    
    def test_incrementar_visualizacao(self):
        """Testa método incrementar_visualizacao"""
        visualizacoes_iniciais = self.produto.visualizacoes
        self.produto.incrementar_visualizacao()
        self.produto.refresh_from_db()
        self.assertEqual(self.produto.visualizacoes, visualizacoes_iniciais + 1)


class ImagemProdutoModelTest(ProdutoTestCase):
    """Testes para o modelo ImagemProduto"""
    
    def create_test_image(self):
        """Cria uma imagem de teste"""
        image = Image.new('RGB', (100, 100), color='red')
        image_file = io.BytesIO()
        image.save(image_file, 'JPEG')
        image_file.seek(0)
        return SimpleUploadedFile(
            'test_image.jpg',
            image_file.getvalue(),
            content_type='image/jpeg'
        )
    
    def test_imagem_produto_creation(self):
        """Testa criação de imagem do produto"""
        test_image = self.create_test_image()
        imagem = ImagemProduto.objects.create(
            produto=self.produto,
            imagem=test_image,
            alt_text='Imagem de teste',
            is_principal=True
        )
        
        self.assertEqual(imagem.produto, self.produto)
        self.assertEqual(imagem.alt_text, 'Imagem de teste')
        self.assertTrue(imagem.is_principal)
    
    def test_imagem_str_method(self):
        """Testa método __str__"""
        test_image = self.create_test_image()
        imagem = ImagemProduto.objects.create(
            produto=self.produto,
            imagem=test_image,
            alt_text='Teste'
        )
        
        expected_str = f"Imagem - {self.produto.nome}"
        self.assertEqual(str(imagem), expected_str)
    
    def test_imagem_principal_unica(self):
        """Testa que apenas uma imagem pode ser principal"""
        test_image1 = self.create_test_image()
        test_image2 = self.create_test_image()
        
        imagem1 = ImagemProduto.objects.create(
            produto=self.produto,
            imagem=test_image1,
            alt_text='Imagem 1',
            is_principal=True
        )
        
        imagem2 = ImagemProduto.objects.create(
            produto=self.produto,
            imagem=test_image2,
            alt_text='Imagem 2',
            is_principal=True
        )
        
        # Recarregar do banco
        imagem1.refresh_from_db()
        imagem2.refresh_from_db()
        
        # Apenas a segunda deve ser principal
        self.assertFalse(imagem1.is_principal)
        self.assertTrue(imagem2.is_principal)


class AvaliacaoModelTest(ProdutoTestCase):
    """Testes para o modelo Avaliacao"""
    
    def test_avaliacao_creation(self):
        """Testa criação de avaliação"""
        avaliacao = Avaliacao.objects.create(
            produto=self.produto,
            usuario=self.user,
            nota=5,
            titulo='Excelente produto',
            comentario='Meu cão adorou esta ração!'
        )
        
        self.assertEqual(avaliacao.produto, self.produto)
        self.assertEqual(avaliacao.usuario, self.user)
        self.assertEqual(avaliacao.nota, 5)
        self.assertTrue(avaliacao.aprovado)
    
    def test_avaliacao_str_method(self):
        """Testa método __str__"""
        avaliacao = Avaliacao.objects.create(
            produto=self.produto,
            usuario=self.user,
            nota=4,
            comentario='Bom produto'
        )
        
        expected_str = f"{self.user.username} - {self.produto.nome} (4★)"
        self.assertEqual(str(avaliacao), expected_str)
    
    def test_avaliacao_unica_por_usuario(self):
        """Testa que usuário só pode avaliar uma vez por produto"""
        Avaliacao.objects.create(
            produto=self.produto,
            usuario=self.user,
            nota=5,
            comentario='Primeira avaliação'
        )
        
        with self.assertRaises(IntegrityError):
            Avaliacao.objects.create(
                produto=self.produto,
                usuario=self.user,
                nota=3,
                comentario='Segunda avaliação'
            )
    
    def test_media_avaliacoes_produto(self):
        """Testa cálculo de média de avaliações"""
        # Criar usuário adicional
        user2 = User.objects.create_user(
            username='user2',
            email='user2@test.com',
            password='pass123'
        )
        
        # Criar avaliações
        Avaliacao.objects.create(produto=self.produto, usuario=self.user, nota=5, comentario='Ótimo')
        Avaliacao.objects.create(produto=self.produto, usuario=user2, nota=3, comentario='Regular')
        
        # Média deve ser 4.0
        self.assertEqual(self.produto.media_avaliacoes, 4.0)
        self.assertEqual(self.produto.total_avaliacoes, 2)


class ListaModelTest(ProdutoTestCase):
    """Testes para o modelo Lista"""
    
    def test_lista_creation(self):
        """Testa criação de lista"""
        lista = Lista.objects.create(
            usuario=self.user,
            tipo='favoritos',
            nome='Meus Favoritos'
        )
        
        lista.produtos.add(self.produto)
        
        self.assertEqual(lista.usuario, self.user)
        self.assertEqual(lista.tipo, 'favoritos')
        self.assertEqual(lista.total_produtos, 1)
    
    def test_lista_str_method(self):
        """Testa método __str__"""
        lista = Lista.objects.create(
            usuario=self.user,
            tipo='desejos',
            nome='Lista de Desejos'
        )
        
        expected_str = f"Lista de Desejos - {self.user.username}"
        self.assertEqual(str(lista), expected_str)
    
    def test_lista_unica_por_tipo_usuario(self):
        """Testa que usuário só pode ter uma lista por tipo"""
        Lista.objects.create(
            usuario=self.user,
            tipo='favoritos'
        )
        
        with self.assertRaises(IntegrityError):
            Lista.objects.create(
                usuario=self.user,
                tipo='favoritos'
            )


class ProdutoViewsTest(ProdutoTestCase):
    """Testes para as views de produtos"""
    
    def test_produto_list_view(self):
        """Testa view de lista de produtos"""
        url = reverse('produtos:lista')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.produto.nome)
        self.assertIn('produtos', response.context)
        self.assertEqual(len(response.context['produtos']), 1)
    
    def test_produto_list_view_with_filters(self):
        """Testa view de lista com filtros"""
        url = reverse('produtos:lista')
        
        # Filtro por categoria
        response = self.client.get(url, {'categoria': self.categoria.slug})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.produto.nome)
        
        # Filtro por marca
        response = self.client.get(url, {'marca': self.marca.slug})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.produto.nome)
        
        # Filtro por preço
        response = self.client.get(url, {'preco_min': '40', 'preco_max': '60'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.produto.nome)
        
        # Filtro que não deveria retornar resultados
        response = self.client.get(url, {'preco_min': '100'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.produto.nome)
    
    def test_produto_detail_view(self):
        """Testa view de detalhes do produto"""
        url = reverse('produtos:detalhe', kwargs={'slug': self.produto.slug})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.produto.nome)
        self.assertContains(response, self.produto.descricao)
        self.assertEqual(response.context['produto'], self.produto)
    
    def test_produto_detail_view_404(self):
        """Testa view de detalhes com produto inexistente"""
        url = reverse('produtos:detalhe', kwargs={'slug': 'produto-inexistente'})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 404)
    
    def test_categoria_detail_view(self):
        """Testa view de detalhes da categoria"""
        url = reverse('produtos:categoria', kwargs={'slug': self.categoria.slug})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.categoria.nome)
        self.assertContains(response, self.produto.nome)
        self.assertEqual(response.context['categoria'], self.categoria)
    
    def test_marca_detail_view(self):
        """Testa view de detalhes da marca"""
        url = reverse('produtos:marca', kwargs={'slug': self.marca.slug})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.marca.nome)
        self.assertContains(response, self.produto.nome)
        self.assertEqual(response.context['marca'], self.marca)
    
    def test_buscar_produtos_view(self):
        """Testa view de busca"""
        url = reverse('produtos:buscar')
        
        # Busca com resultados
        response = self.client.get(url, {'q': 'ração'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.produto.nome)
        
        # Busca sem resultados
        response = self.client.get(url, {'q': 'produto inexistente'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.produto.nome)
    
    def test_buscar_produtos_ajax(self):
        """Testa busca via AJAX"""
        url = reverse('produtos:buscar')
        response = self.client.get(
            url, 
            {'q': 'ração'}, 
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        
        data = json.loads(response.content)
        self.assertIn('produtos', data)
        self.assertEqual(len(data['produtos']), 1)
        self.assertEqual(data['produtos'][0]['nome'], self.produto.nome)
    
    def test_adicionar_avaliacao_view(self):
        """Testa view de adicionar avaliação"""
        self.client.login(username='testuser', password='testpass123')
        
        url = reverse('produtos:adicionar_avaliacao', kwargs={'produto_slug': self.produto.slug})
        response = self.client.post(url, {
            'nota': 5,
            'titulo': 'Excelente!',
            'comentario': 'Produto muito bom, recomendo!'
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect após POST
        
        # Verificar se avaliação foi criada
        avaliacao = Avaliacao.objects.get(produto=self.produto, usuario=self.user)
        self.assertEqual(avaliacao.nota, 5)
        self.assertEqual(avaliacao.titulo, 'Excelente!')
    
    def test_adicionar_avaliacao_duplicada(self):
        """Testa tentativa de adicionar avaliação duplicada"""
        self.client.login(username='testuser', password='testpass123')
        
        # Criar primeira avaliação
        Avaliacao.objects.create(
            produto=self.produto,
            usuario=self.user,
            nota=4,
            comentario='Primeira avaliação'
        )
        
        # Tentar criar segunda avaliação
        url = reverse('produtos:adicionar_avaliacao', kwargs={'produto_slug': self.produto.slug})
        response = self.client.post(url, {
            'nota': 5,
            'comentario': 'Segunda avaliação'
        })
        
        self.assertEqual(response.status_code, 302)
        # Verificar que apenas uma avaliação existe
        self.assertEqual(Avaliacao.objects.filter(produto=self.produto, usuario=self.user).count(), 1)
    
    def test_adicionar_ao_carrinho_view(self):
        """Testa view de adicionar ao carrinho"""
        self.client.login(username='testuser', password='testpass123')
        
        url = reverse('produtos:ajax_adicionar_carrinho')
        response = self.client.post(url, {
            'produto_id': self.produto.id,
            'quantidade': 2
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect após POST
        
        # # Verificar se item foi adicionado ao carrinho
        # carrinho = Carrinho.objects.get(usuario=self.user)
        # item = ItemCarrinho.objects.get(carrinho=carrinho, produto=self.produto)
        # self.assertEqual(item.quantidade, 2)
    
    def test_adicionar_ao_carrinho_ajax(self):
        """Testa adicionar ao carrinho via AJAX"""
        self.client.login(username='testuser', password='testpass123')
        
        url = reverse('produtos:ajax_adicionar_carrinho')
        response = self.client.post(
            url, 
            {
                'produto_id': self.produto.id,
                'quantidade': 1
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertIn('message', data)
        self.assertIn('carrinho', data)


class ProdutoFormsTest(ProdutoTestCase):
    """Testes para os formulários"""
    
    def test_busca_form_valid(self):
        """Testa formulário de busca válido"""
        form_data = {'q': 'ração premium'}
        form = BuscaForm(data=form_data)
        
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['q'], 'ração premium')
    
    def test_busca_form_termo_muito_curto(self):
        """Testa formulário de busca com termo muito curto"""
        form_data = {'q': 'r'}
        form = BuscaForm(data=form_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('Digite pelo menos 2 caracteres', str(form.errors['q']))
    
    def test_produto_filter_form(self):
        """Testa formulário de filtros"""
        form_data = {
            'categoria': self.categoria.id,
            'marca': self.marca.id,
            'preco_min': '10.00',
            'preco_max': '100.00',
            'tipo_animal': 'cao',
            'promocao': True
        }
        form = ProdutoFilterForm(data=form_data)
        
        self.assertTrue(form.is_valid())
    
    def test_produto_filter_form_preco_invalido(self):
        """Testa formulário com faixa de preço inválida"""
        form_data = {
            'preco_min': '100.00',
            'preco_max': '50.00'  # Máximo menor que mínimo
        }
        form = ProdutoFilterForm(data=form_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('Preço mínimo não pode ser maior que o máximo', str(form.errors['__all__']))
    
    def test_avaliacao_form_valid(self):
        """Testa formulário de avaliação válido"""
        form_data = {
            'nota': 5,
            'titulo': 'Excelente produto',
            'comentario': 'Produto de qualidade excepcional, recomendo muito!'
        }
        form = AvaliacaoForm(data=form_data)
        
        self.assertTrue(form.is_valid())
    
    def test_avaliacao_form_comentario_muito_curto(self):
        """Testa formulário com comentário muito curto"""
        form_data = {
            'nota': 5,
            'comentario': 'Muito bom'  # Menos de 10 caracteres
        }
        form = AvaliacaoForm(data=form_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('pelo menos 10 caracteres', str(form.errors['comentario']))
    
    def test_adicionar_carrinho_form(self):
        """Testa formulário de adicionar ao carrinho"""
        form_data = {
            'produto_id': self.produto.id,
            'quantidade': 2
        }
        form = AdicionarCarrinhoForm(produto=self.produto, data=form_data)
        
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['quantidade'], 2)
    
    def test_adicionar_carrinho_form_quantidade_invalida(self):
        """Testa formulário com quantidade inválida"""
        form_data = {
            'produto_id': self.produto.id,
            'quantidade': 0  # Quantidade inválida
        }
        form = AdicionarCarrinhoForm(produto=self.produto, data=form_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('maior que zero', str(form.errors['quantidade']))


class ProdutoIntegrationTest(ProdutoTestCase):
    """Testes de integração"""
    
    def test_fluxo_completo_produto(self):
        """Testa fluxo completo: visualizar produto -> avaliar -> adicionar ao carrinho"""
        self.client.login(username='testuser', password='testpass123')
        
        # 1. Visualizar produto
        url_detalhe = reverse('produtos:detalhe', kwargs={'slug': self.produto.slug})
        response = self.client.get(url_detalhe)
        self.assertEqual(response.status_code, 200)
        
        # Verificar se visualização foi incrementada
        self.produto.refresh_from_db()
        self.assertEqual(self.produto.visualizacoes, 1)
        
        # 2. Adicionar avaliação
        url_avaliacao = reverse('produtos:adicionar_avaliacao', kwargs={'produto_slug': self.produto.slug})
        response = self.client.post(url_avaliacao, {
            'nota': 5,
            'comentario': 'Produto excelente, meu pet adorou!'
        })
        self.assertEqual(response.status_code, 302)
        
        # Verificar avaliação criada
        self.assertTrue(Avaliacao.objects.filter(produto=self.produto, usuario=self.user).exists())
        
        # 3. Adicionar ao carrinho
        url_carrinho = reverse('produtos:ajax_adicionar_carrinho')
        response = self.client.post(url_carrinho, {
            'produto_id': self.produto.id,
            'quantidade': 1
        })
        self.assertEqual(response.status_code, 302)
        
        # Verificar item no carrinho
        # self.assertTrue(ItemCarrinho.objects.filter(
        #     carrinho__usuario=self.user,
        #     produto=self.produto
        # ).exists())
    
    def test_busca_e_filtros_integrados(self):
        """Testa busca combinada com filtros"""
        # Criar produtos adicionais para teste
        categoria_brinquedos = Categoria.objects.create(nome='Brinquedos', ativo=True)
        marca_kong = Marca.objects.create(nome='Kong', ativo=True)
        
        Produto.objects.create(
            nome='Brinquedo Kong para Cães',
            categoria=categoria_brinquedos,
            marca=marca_kong,
            preco=Decimal('25.90'),
            ativo=True,
            tipo_animal='cao'
        )
        
        # Buscar com filtros
        url = reverse('produtos:lista')
        response = self.client.get(url, {
            'q': 'cão',
            'categoria': categoria_brinquedos.slug,
            'preco_max': '30.00'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Brinquedo Kong')
        self.assertNotContains(response, 'Ração Pedigree')  # Categoria diferente



class ProdutoTestRunner:
    """Runner customizado para organizar execução dos testes"""
    
    @classmethod
    def run_model_tests(cls):
        """Executa apenas testes de models"""
        from django.test.utils import get_runner
        from django.conf import settings
        
        TestRunner = get_runner(settings)
        test_runner = TestRunner()
        
        failures = test_runner.run_tests([
            'apps.produtos.tests.CategoriaModelTest',
            'apps.produtos.tests.MarcaModelTest',
            'apps.produtos.tests.ProdutoModelTest',
            'apps.produtos.tests.ImagemProdutoModelTest',
            'apps.produtos.tests.AvaliacaoModelTest',
            'apps.produtos.tests.ListaModelTest'
        ])
        
        return failures
    
    @classmethod
    def run_view_tests(cls):
        """Executa apenas testes de views"""
        from django.test.utils import get_runner
        from django.conf import settings
        
        TestRunner = get_runner(settings)
        test_runner = TestRunner()
        
        failures = test_runner.run_tests([
            'apps.produtos.tests.ProdutoViewsTest'
        ])
        
        return failures


if __name__ == '__main__':
    # Execução direta do arquivo de testes
    import django
    from django.conf import settings
    from django.test.utils import get_runner
    
    if not settings.configured:
        settings.configure(
            DEBUG=True,
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': ':memory:',
                }
            },
            INSTALLED_APPS=[
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'apps.produtos',
                'apps.carrinho',
            ]
        )
    
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(['apps.produtos.tests'])
