from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Banner, Categoria, Beneficio, ServicoDestaque, Oferta


class HomeView(TemplateView):
    """View da página inicial"""
    template_name = 'core/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Banners do carrossel
        context['banners'] = Banner.objects.filter(ativo=True)[:4]
        
        # Benefícios (Entrega Expressa, Frete Grátis, etc)
        context['beneficios'] = Beneficio.objects.filter(ativo=True)
        
        # Mais Procurados
        context['mais_procurados'] = Categoria.objects.filter(
            tipo='mais_procurado',
            ativo=True
        )[:6]
        
        # Categorias por Espécies
        context['categorias_especies'] = Categoria.objects.filter(
            tipo='especie',
            ativo=True
        )[:6]
        
        # Serviços em Destaque
        context['servicos_destaque'] = ServicoDestaque.objects.filter(ativo=True)[:3]
        
        # Oferta Ativa
        ofertas = Oferta.objects.filter(ativo=True)
        context['oferta'] = next((o for o in ofertas if o.esta_ativa), None)
        
        return context


def produtos(request):
    """View para página de produtos (placeholder)"""
    return render(request, 'core/produtos.html', {
        'titulo': 'Produtos - Smart Paws'
    })


def servicos(request):
    """View para página de serviços (placeholder)"""
    return render(request, 'core/servicos.html', {
        'titulo': 'Serviços - Smart Paws'
    })


def adocao(request):
    """View para página de adoção (placeholder)"""
    return render(request, 'core/adocao.html', {
        'titulo': 'Adoção - Smart Paws'
    })

# def usuario(request):
#     return render(request, 'templates/usuarios/paginalogin.html',{
#         'titulo': 'Pagina  login - SmartPaws'


#     })