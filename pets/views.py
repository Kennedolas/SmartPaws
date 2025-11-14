# ==========================================
# pets/views.py - VERSÃO CORRIGIDA
# ==========================================

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Pet, SolicitacaoAdocao, PromocaoAdocao
from .forms import SolicitacaoAdocaoForm


def adocao(request):
    """Página principal de adoção"""
    # Buscar pets disponíveis
    pets = Pet.objects.filter(status='disponivel')
    
    # Filtros
    ordenacao = request.GET.get('ordem', '-created_at')
    
    if ordenacao == 'recentes':
        pets = pets.order_by('-created_at')
    elif ordenacao == 'antigos':
        pets = pets.order_by('created_at')
    
    # Filtro por espécie, porte, sexo
    especie = request.GET.get('especie')
    if especie:
        pets = pets.filter(especie=especie)
    
    porte = request.GET.get('porte')
    if porte:
        pets = pets.filter(porte=porte)
    
    sexo = request.GET.get('sexo')
    if sexo:
        pets = pets.filter(sexo=sexo)
    
    context = {
        'pets': pets,
        'ordenacao_atual': ordenacao,
    }
    
    return render(request, 'pets/adocao.html', context)


def detalhe_pet(request, slug):
    """Detalhes de um pet específico"""
    pet = get_object_or_404(Pet, slug=slug, status__in=['disponivel', 'processo'])
    
    # Buscar pets similares
    pets_similares = Pet.objects.filter(
        status='disponivel',
        especie=pet.especie
    ).exclude(id=pet.id)[:4]
    
    context = {
        'pet': pet,
        'pets_similares': pets_similares,
    }
    
    return render(request, 'pets/detalhes_pets.html', context)


@login_required
def solicitar_adocao(request, slug):
    """Formulário de solicitação de adoção"""
    pet = get_object_or_404(Pet, slug=slug, status='disponivel')
    
    # Verificar se já existe solicitação pendente do usuário para este pet
    solicitacao_existente = SolicitacaoAdocao.objects.filter(
        pet=pet,
        usuario=request.user,
        status='pendente'
    ).exists()
    
    if solicitacao_existente:
        messages.warning(request, 'Você já possui uma solicitação pendente para este pet.')
        return redirect('pets:detalhe', slug=pet.slug)
    
    if request.method == 'POST':
        form = SolicitacaoAdocaoForm(request.POST)
        if form.is_valid():
            solicitacao = form.save(commit=False)
            solicitacao.pet = pet
            solicitacao.usuario = request.user
            solicitacao.save()
            
            messages.success(request, 'Solicitação de adoção enviada com sucesso! Entraremos em contato em breve.')
            return redirect('pets:minhas_solicitacoes')
    else:
        # Preencher dados iniciais com informações do usuário
        initial_data = {
            'nome_completo': request.user.get_full_name() or f"{request.user.first_name} {request.user.last_name}",
            'email': request.user.email,
            'telefone': getattr(request.user, 'telefone', ''),
        }
        form = SolicitacaoAdocaoForm(initial=initial_data)
    
    context = {
        'form': form,
        'pet': pet,
    }
    
    return render(request, 'pets/solicitar_adocao.html', context)


@login_required
def minhas_solicitacoes(request):
    """Lista de solicitações de adoção do usuário"""
    solicitacoes = SolicitacaoAdocao.objects.filter(
        usuario=request.user
    ).select_related('pet').order_by('-created_at')
    
    context = {
        'solicitacoes': solicitacoes,
    }
    
    return render(request, 'pets/minhas_solicitacoes.html', context)


def buscar_pets(request):
    """Busca de pets com filtros"""
    query = request.GET.get('q', '')
    
    pets = Pet.objects.filter(status='disponivel')
    
    if query:
        pets = pets.filter(
            Q(nome__icontains=query) |
            Q(raca__icontains=query) |
            Q(descricao__icontains=query) |
            Q(temperamento__icontains=query)
        )
    
    context = {
        'pets': pets,
        'query': query,
    }
    
    return render(request, 'pets/buscar_pets.html', context)


def promocoes_adocao(request):
    """Lista de promoções ativas"""
    promocoes = PromocaoAdocao.objects.filter(ativo=True).order_by('-data_inicio')
    
    context = {
        'promocoes': promocoes,
    }
    
    return render(request, 'pets/promocoes.html', context)


def detalhe_promocao(request, slug):
    """Detalhes de uma promoção"""
    promocao = get_object_or_404(PromocaoAdocao, slug=slug, ativo=True)
    
    # Buscar pets disponíveis para essa promoção (opcional)
    pets = Pet.objects.filter(status='disponivel')[:8]
    
    context = {
        'promocao': promocao,
        'pets': pets,
    }
    
    return render(request, 'pets/detalhe_promocao.html', context)
