from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import PetAdocao, SolicitacaoAdocao

User = get_user_model()


class PetAdocaoModelTest(TestCase):
    """Testes do model PetAdocao"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='nicolly',
            email='nicolly1234@gmail.com',
            password='123'
        )
        
        self.pet = PetAdocao.objects.create(
            nome='joao gordo',
            especie='cachorro',
            sexo='macho',
            porte='grande',
            idade_categoria='adulto',
            idade_meses=36,
            descricao='Cachorro dócil',
            cidade='São Paulo',
            estado='SP',
            doador=self.user,
            contato_doador='619999999'
        )
    
    def test_criacao_pet(self):
        """Testa criação de pet"""
        self.assertEqual(self.pet.nome, 'Rex')
        self.assertFalse(self.pet.adotado)
        self.assertTrue(self.pet.ativo)
    
    def test_slug_automatico(self):
        """Testa geração de slug"""
        self.assertEqual(self.pet.slug, 'rex')
    
    def test_idade_formatada(self):
        """Testa formatação de idade"""
        self.assertEqual(self.pet.idade_formatada, '3 ano(s) e 0 mês(es)')
    
    def test_incrementar_visualizacao(self):
        """Testa incremento de visualizações"""
        views_inicial = self.pet.visualizacoes
        self.pet.incrementar_visualizacao()
        self.assertEqual(self.pet.visualizacoes, views_inicial + 1)


class PetAdocaoViewsTest(TestCase):
    """Testes das views"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Criar pets de teste
        for i in range(5):
            PetAdocao.objects.create(
                nome=f'Pet {i}',
                especie='cachorro',
                sexo='macho',
                porte='medio',
                idade_categoria='adulto',
                idade_meses=24,
                descricao='Teste',
                cidade='São Paulo',
                estado='SP',
                doador=self.user,
                contato_doador='11999999999'
            )
    
    def test_lista_pets(self):
        """Testa listagem de pets"""
        response = self.client.get(reverse('adocao:lista'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Pet')
    
    def test_detalhe_pet(self):
        """Testa página de detalhe"""
        pet = PetAdocao.objects.first()
        response = self.client.get(
            reverse('adocao:detalhe', kwargs={'slug': pet.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, pet.nome)