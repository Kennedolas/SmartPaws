# ==========================================
# servicos/views.py
# ==========================================

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Servico, CategoriaServico, Prestador, AgendamentoServico
from .forms import AgendamentoServicoForm


def lista_servicos(request):
    """Lista de serviços com filtros"""
    servicos = Servico.objects.filter(ativo=True).select_related('prestador', 'categoria')
    
    # Filtro por categoria
    categoria_slug = request.GET.get('categoria')
    if categoria_slug:
        servicos = servicos.filter(categoria__slug=categoria_slug)
    
    # Filtro por prestador
    prestador_slug = request.GET.get('prestador')
    if prestador_slug:
        servicos = servicos.filter(prestador__slug=prestador_slug)
    
    # Filtro por faixa de preço
    preco_min = request.GET.get('preco_min')
    preco_max = request.GET.get('preco_max')
    if preco_min:
        servicos = servicos.filter(preco__gte=preco_min)
    if preco_max:
        servicos = servicos.filter(preco__lte=preco_max)
    
    # Busca por nome
    query = request.GET.get('q')
    if query:
        servicos = servicos.filter(
            Q(nome__icontains=query) |
            Q(descricao__icontains=query) |
            Q(prestador__nome__icontains=query)
        )
    
    # Ordenação
    ordem = request.GET.get('ordem', '-destaque')
    if ordem == 'preco_menor':
        servicos = servicos.order_by('preco')
    elif ordem == 'preco_maior':
        servicos = servicos.order_by('-preco')
    elif ordem == 'nome':
        servicos = servicos.order_by('nome')
    elif ordem == 'avaliacao':
        servicos = servicos.order_by('-prestador__avaliacao_media')
    else:
        servicos = servicos.order_by('-destaque', '-created_at')
    
    # Categorias e prestadores para filtros
    categorias = CategoriaServico.objects.filter(ativo=True)
    prestadores = Prestador.objects.filter(ativo=True)
    
    context = {
        'servicos': servicos,
        'categorias': categorias,
        'prestadores': prestadores,
        'categoria_atual': categoria_slug,
        'prestador_atual': prestador_slug,
        'query': query,
        'ordem_atual': ordem,
    }
    
    return render(request, 'servicos/lista.html', context)


def detalhe_servico(request, slug):
    """Detalhes de um serviço"""
    servico = get_object_or_404(
        Servico.objects.select_related('prestador', 'categoria'),
        slug=slug,
        ativo=True
    )
    
    # Serviços relacionados do mesmo prestador
    servicos_relacionados = Servico.objects.filter(
        prestador=servico.prestador,
        ativo=True
    ).exclude(id=servico.id)[:4]
    
    context = {
        'servico': servico,
        'servicos_relacionados': servicos_relacionados,
    }
    
    return render(request, 'servicos/detalhe.html', context)


@login_required
def agendar_servico(request, slug):
    """Agendar um serviço"""
    servico = get_object_or_404(Servico, slug=slug, ativo=True)
    
    if request.method == 'POST':
        form = AgendamentoServicoForm(request.POST)
        if form.is_valid():
            agendamento = form.save(commit=False)
            agendamento.usuario = request.user
            agendamento.servico = servico
            agendamento.save()
            
            messages.success(request, 'Agendamento realizado com sucesso! O prestador entrará em contato.')
            return redirect('servicos:meus_agendamentos')
    else:
        form = AgendamentoServicoForm()
    
    context = {
        'servico': servico,
        'form': form,
    }
    
    return render(request, 'servicos/agendar.html', context)


@login_required
def meus_agendamentos(request):
    """Lista de agendamentos do usuário"""
    agendamentos = AgendamentoServico.objects.filter(
        usuario=request.user
    ).select_related('servico', 'servico__prestador').order_by('-created_at')
    
    context = {
        'agendamentos': agendamentos,
    }
    
    return render(request, 'servicos/meus_agendamentos.html', context)


def lista_prestadores(request):
    """Lista de prestadores"""
    prestadores = Prestador.objects.filter(ativo=True)
    
    # Filtro por cidade
    cidade = request.GET.get('cidade')
    if cidade:
        prestadores = prestadores.filter(cidade__icontains=cidade)
    
    # Ordenação
    ordem = request.GET.get('ordem', '-destaque')
    if ordem == 'avaliacao':
        prestadores = prestadores.order_by('-avaliacao_media')
    elif ordem == 'nome':
        prestadores = prestadores.order_by('nome')
    else:
        prestadores = prestadores.order_by('-destaque', '-avaliacao_media')
    
    context = {
        'prestadores': prestadores,
        'ordem_atual': ordem,
    }
    
    return render(request, 'servicos/prestadores.html', context)


def detalhe_prestador(request, slug):
    """Detalhes de um prestador"""
    prestador = get_object_or_404(Prestador, slug=slug, ativo=True)
    servicos = prestador.servicos.filter(ativo=True)
    
    context = {
        'prestador': prestador,
        'servicos': servicos,
    }
    
    return render(request, 'servicos/detalhe_prestador.html', context)
