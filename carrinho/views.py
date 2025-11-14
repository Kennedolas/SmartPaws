from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import transaction
from decimal import Decimal
from .models import Carrinho, ItemCarrinho, Pedido, ItemPedido
from produtos.models import Produto
import json


def get_or_create_carrinho(user):
    """Obtém ou cria carrinho do usuário"""
    carrinho, created = Carrinho.objects.get_or_create(usuario=user)
    return carrinho


@login_required
def adicionar_ao_carrinho(request, produto_id):
    """Adiciona produto ao carrinho"""
    produto = get_object_or_404(Produto, id=produto_id, ativo=True)
    carrinho = get_or_create_carrinho(request.user)
    
    quantidade = int(request.POST.get('quantidade', 1))
    
    # Verifica se já existe no carrinho
    item, created = ItemCarrinho.objects.get_or_create(
        carrinho=carrinho,
        produto=produto,
        defaults={'quantidade': quantidade, 'preco_unitario': produto.preco_final}
    )
    
    if not created:
        # Atualiza quantidade
        item.quantidade += quantidade
        item.save()
    
    messages.success(request, f'{produto.nome} adicionado ao carrinho!')
    
    # Retorna JSON se for requisição AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'total_itens': carrinho.total_itens,
            'message': f'{produto.nome} adicionado ao carrinho!'
        })
    
    return redirect('carrinho:visualizar')


@login_required
def visualizar_carrinho(request):
    """Visualiza carrinho"""
    carrinho = get_or_create_carrinho(request.user)
    itens = carrinho.itens.select_related('produto').all()
    
    frete_gratis_minimo = 200
    falta_frete_gratis = max(0, frete_gratis_minimo - float(carrinho.subtotal))
    context = {
        'carrinho': carrinho,
        'itens': itens,
        'falta_frete_gratis': falta_frete_gratis,
    }
    
    return render(request, 'carrinho/visualizar.html', context)


@login_required
@require_POST
def atualizar_quantidade(request, item_id):
    """Atualiza quantidade de um item"""
    item = get_object_or_404(ItemCarrinho, id=item_id, carrinho__usuario=request.user)
    quantidade = int(request.POST.get('quantidade', 1))
    
    if quantidade > 0:
        item.quantidade = quantidade
        item.save()
        
        return JsonResponse({
            'success': True,
            'item_total': float(item.total),
            'carrinho_subtotal': float(item.carrinho.subtotal),
            'carrinho_total': float(item.carrinho.total)
        })
    
    return JsonResponse({'success': False, 'error': 'Quantidade inválida'})


@login_required
@require_POST
def remover_item(request, item_id):
    """Remove item do carrinho"""
    item = get_object_or_404(ItemCarrinho, id=item_id, carrinho__usuario=request.user)
    produto_nome = item.produto.nome
    item.delete()
    
    messages.success(request, f'{produto_nome} removido do carrinho!')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        carrinho = get_or_create_carrinho(request.user)
        return JsonResponse({
            'success': True,
            'total_itens': carrinho.total_itens,
            'carrinho_subtotal': float(carrinho.subtotal),
            'carrinho_total': float(carrinho.total)
        })
    
    return redirect('carrinho:visualizar')


@login_required
def limpar_carrinho(request):
    """Limpa todo o carrinho"""
    carrinho = get_or_create_carrinho(request.user)
    carrinho.itens.all().delete()
    
    messages.success(request, 'Carrinho limpo!')
    return redirect('carrinho:visualizar')


@login_required
def checkout(request):
    """Página de checkout"""
    carrinho = get_or_create_carrinho(request.user)
    itens = carrinho.itens.select_related('produto').all()
    
    if not itens:
        messages.warning(request, 'Seu carrinho está vazio!')
        return redirect('produtos:lista')
    
    # Busca endereços do usuário (se tiver)
    enderecos = request.user.enderecos.all() if hasattr(request.user, 'enderecos') else []
    
    context = {
        'carrinho': carrinho,
        'itens': itens,
        'enderecos': enderecos,
    }
    
    return render(request, 'carrinho/checkout.html', context)


@login_required
@transaction.atomic
def finalizar_pedido(request):
    """Finaliza pedido e processa pagamento"""
    if request.method != 'POST':
        return redirect('carrinho:checkout')
    
    carrinho = get_or_create_carrinho(request.user)
    itens = carrinho.itens.select_related('produto').all()
    
    if not itens:
        messages.error(request, 'Seu carrinho está vazio!')
        return redirect('produtos:lista')
    
    # Dados do formulário
    endereco_entrega = request.POST.get('endereco_entrega')
    forma_pagamento = request.POST.get('forma_pagamento')
    observacoes = request.POST.get('observacoes', '')
    
    # Cria o pedido
    pedido = Pedido.objects.create(
        usuario=request.user,
        subtotal=carrinho.subtotal,
        desconto=carrinho.desconto,
        frete=carrinho.frete,
        total=carrinho.total,
        endereco_entrega=endereco_entrega,
        forma_pagamento=forma_pagamento,
        observacoes=observacoes
    )
    
    # Cria itens do pedido
    for item in itens:
        ItemPedido.objects.create(
            pedido=pedido,
            produto=item.produto,
            nome_produto=item.produto.nome,
            quantidade=item.quantidade,
            preco_unitario=item.preco_unitario,
            subtotal=item.total
        )
    
    # Processa pagamento
    if forma_pagamento == 'pix':
        # Gera QR Code PIX (mock - integrar com gateway real)
        pedido.qr_code_pix = f"00020126580014BR.GOV.BCB.PIX0136{pedido.numero_pedido}520400005303986540{pedido.total}5802BR5913SmartPaws6009SAO PAULO62070503***6304"
        pedido.save()
    
    # Limpa carrinho
    carrinho.itens.all().delete()
    
    messages.success(request, f'Pedido #{pedido.numero_pedido} criado com sucesso!')
    return redirect('carrinho:pedido_confirmado', pedido_id=pedido.id)


@login_required
def pedido_confirmado(request, pedido_id):
    """Página de confirmação do pedido"""
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    
    context = {
        'pedido': pedido,
    }
    
    return render(request, 'carrinho/pedido_confirmado.html', context)


@login_required
def meus_pedidos(request):
    """Lista pedidos do usuário"""
    pedidos = Pedido.objects.filter(usuario=request.user).prefetch_related('itens')
    
    context = {
        'pedidos': pedidos,
    }
    
    return render(request, 'carrinho/meus_pedidos.html', context)


@login_required
def detalhe_pedido(request, pedido_id):
    """Detalhes de um pedido"""
    pedido = get_object_or_404(
        Pedido.objects.prefetch_related('itens'),
        id=pedido_id,
        usuario=request.user
    )
    
    context = {
        'pedido': pedido,
    }
    
    return render(request, 'carrinho/detalhe_pedido.html', context)


# AJAX - Contador do carrinho no header
@login_required
def carrinho_count(request):
    """Retorna quantidade de itens no carrinho (AJAX)"""
    carrinho = get_or_create_carrinho(request.user)
    return JsonResponse({'count': carrinho.total_itens})