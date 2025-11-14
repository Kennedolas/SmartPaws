# ==========================================
# produtos/views.py
# ==========================================

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q, Count, Avg
from .models import Produto, CategoriaProduto
from .forms import ProdutoFiltroForm


class ProdutoListView(ListView):
    """Lista de produtos com filtros avançados"""
    model = Produto
    template_name = 'produtos/lista.html'
    context_object_name = 'produtos'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Produto.objects.filter(ativo=True).select_related('categoria')
        
        # Parâmetros do filtro
        busca = self.request.GET.get('busca', '').strip()
        categoria_id = self.request.GET.get('categoria')
        preco_min = self.request.GET.get('preco_min')
        preco_max = self.request.GET.get('preco_max')
        em_promocao = self.request.GET.get('em_promocao')
        ordenar = self.request.GET.get('ordenar', 'relevancia')
        
        # Filtro de busca
        if busca:
            queryset = queryset.filter(
                Q(nome__icontains=busca) |
                Q(descricao__icontains=busca) |
                Q(categoria__nome__icontains=busca)
            )
        
        # Filtro por categoria
        if categoria_id:
            queryset = queryset.filter(categoria_id=categoria_id)
        
        # Filtro por preço
        if preco_min:
            queryset = queryset.filter(preco_original__gte=preco_min)
        if preco_max:
            queryset = queryset.filter(preco_original__lte=preco_max)
        
        # Filtro de promoção
        if em_promocao:
            queryset = queryset.filter(preco_desconto__isnull=False)
        
        # Ordenação
        if ordenar == 'menor_preco':
            queryset = queryset.order_by('preco_original')
        elif ordenar == 'maior_preco':
            queryset = queryset.order_by('-preco_original')
        elif ordenar == 'melhor_avaliacao':
            queryset = queryset.order_by('-avaliacao', '-numero_avaliacoes')
        elif ordenar == 'nome_az':
            queryset = queryset.order_by('nome')
        elif ordenar == 'nome_za':
            queryset = queryset.order_by('-nome')
        else:  # relevancia ou mais_vendidos
            queryset = queryset.order_by('-destaque', '-created_at')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Formulário de filtros
        context['form_filtro'] = ProdutoFiltroForm(self.request.GET)
        
        # Todas as categorias
        context['categorias'] = CategoriaProduto.objects.filter(ativo=True).annotate(
            total_produtos=Count('produtos', filter=Q(produtos__ativo=True))
        )
        
        # Produtos em destaque
        context['produtos_destaque'] = Produto.objects.filter(
            ativo=True, 
            destaque=True
        )[:4]
        
        # Estatísticas
        context['total_produtos'] = self.get_queryset().count()
        
        # Parâmetros atuais (para manter filtros ativos)
        context['filtros_ativos'] = {
            'busca': self.request.GET.get('busca', ''),
            'categoria': self.request.GET.get('categoria', ''),
            'preco_min': self.request.GET.get('preco_min', ''),
            'preco_max': self.request.GET.get('preco_max', ''),
            'em_promocao': self.request.GET.get('em_promocao', ''),
            'ordenar': self.request.GET.get('ordenar', 'relevancia'),
        }
        
        return context


class ProdutoDetailView(DetailView):
    """Detalhes do produto"""
    model = Produto
    template_name = 'produtos/detalhe.html'
    context_object_name = 'produto'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return Produto.objects.filter(ativo=True).select_related('categoria')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Produtos relacionados
        context['produtos_relacionados'] = Produto.objects.filter(
            categoria=self.object.categoria,
            ativo=True
        ).exclude(pk=self.object.pk)[:6]
        
        return context
