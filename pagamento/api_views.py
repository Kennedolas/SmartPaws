from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.utils import timezone
from decimal import Decimal

from .models import Endereco, Pedido, ItemPedido, Pagamentos, RastreamentoEntrega
from .serializers import (
    EnderecoSerializer,
    PedidoSerializer,
    PagamentoSerializer,
    RastreamentoSerializer
    
)
from carrinho.models import ItemCarrinho




class EnderecoListCreateAPIView(generics.ListCreateAPIView):

    serializer_class = EnderecoSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Endereco.objects.filter(usuario=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class EnderecoDetailAPIView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = EnderecoSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Endereco.objects.filter(usuario=self.request.user)




class PedidoListAPIView(generics.ListAPIView):

    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Pedido.objects.filter(
            usuario=self.request.user
        ).prefetch_related('itens', 'pagamento', 'rastreamentos')


class PedidoDetailAPIView(generics.RetrieveAPIView):

    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'numero_pedido'
    
    def get_queryset(self):
        return Pedido.objects.filter(usuario=self.request.user)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def criar_pedido(request):

    serializer = PedidoSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Buscar endereço
    endereco = get_object_or_404(
        Endereco,
        id=serializer.validated_data['endereco_id'],
        usuario=request.user
    )
    
    # Buscar itens do carrinho
    itens_carrinho = ItemCarrinho.objects.filter(
        usuario=request.user
    ).select_related('produto', 'produto__loja')
    
    if not itens_carrinho.exists():
        return Response({
            'error': 'Carrinho vazio'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        with transaction.atomic():
            # Calcular valores
            subtotal = sum(item.subtotal for item in itens_carrinho)
            taxa_entrega = Decimal('15.00') if subtotal > 0 else Decimal('0.00')
            total = subtotal + taxa_entrega
            
            # Criar pedido
            pedido = Pedido.objects.create(
                usuario=request.user,
                endereco_entrega=endereco,
                subtotal=subtotal,
                taxa_entrega=taxa_entrega,
                total=total,
                status='aguardando_pagamento',
                observacoes=serializer.validated_data.get('observacoes', '')
            )
            
            # Criar itens do pedido
            for item_carrinho in itens_carrinho:
                # Verificar estoque
                if item_carrinho.produto.estoque < item_carrinho.quantidade:
                    raise Exception(f'Estoque insuficiente para {item_carrinho.produto.nome}')
                
                ItemPedido.objects.create(
                    pedido=pedido,
                    produto=item_carrinho.produto,
                    loja=item_carrinho.produto.loja,
                    nome_produto=item_carrinho.produto.nome,
                    preco_unitario=item_carrinho.produto.preco,
                    quantidade=item_carrinho.quantidade
                )
                
                # Reduzir estoque
                item_carrinho.produto.estoque -= item_carrinho.quantidade
                item_carrinho.produto.save()
            
            # Criar pagamento
            pagamento = Pagamentos.objects.create(
                pedido=pedido,
                forma_pagamento=serializer.validated_data['forma_pagamento'],
                valor=total,
                status='pendente'
            )
            
            # Processar pagamento (SIMULADO)
            if pagamento.forma_pagamento == 'pix':
                # Gerar PIX (simulado)
                pagamento.chave_pix = "pix@smartpaws.com"
                pagamento.qr_code_pix = "data:image/png;base64,iVBORw0KGgoAAAANS..."  # QR Code simulado
                pagamento.save()
            
            elif pagamento.forma_pagamento == 'boleto':
                # Gerar boleto (simulado)
                pagamento.codigo_boleto = "34191.79001 01043.510047 91020.150008 1 84770000002000"
                pagamento.link_boleto = f"https://smartpaws.com/boleto/{pedido.numero_pedido}"
                pagamento.save()
            
            elif pagamento.forma_pagamento in ['cartao_credito', 'cartao_debito']:
                # Processar cartão (simulado - NUNCA salvar dados reais!)
                pagamento.bandeira_cartao = "Visa"  # Detectar pela API
                pagamento.ultimos_digitos = "1234"  # Últimos 4 dígitos
                pagamento.status = 'aprovado'
                pagamento.data_aprovacao = timezone.now()
                pagamento.save()
                
                # Atualizar pedido
                pedido.status = 'pago'
                pedido.data_pagamento = timezone.now()
                pedido.save()
                        
                # Limpar carrinho
                itens_carrinho.delete()
                        
    
                RastreamentoEntrega.objects.create(
                            pedido=pedido,
                            status='Pedido Recebido',
                            descricao='Seu pedido foi recebido e está sendo processado.',
                            localizacao='Centro de Distribuição SmartPaws'
                    )
                        
                        # Retornar pedido criado
                return Response({
                        'message': 'Pedido criado com sucesso!',
                        'pedido': PedidoSerializer(pedido).data
                        }, status=status.HTTP_201_CREATED)
                
    except Exception as e:
                    return Response({
                        'error': str(e)
                    }, status=status.HTTP_400_BAD_REQUEST)


    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    def cancelar_pedido(request, numero_pedido):
     
                pedido = get_object_or_404(
                    Pedido,
                    numero_pedido=numero_pedido,
                    usuario=request.user
                )
                
                if not pedido.pode_cancelar:
                    return Response({
                        'error': 'Este pedido não pode ser cancelado'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                with transaction.atomic():
                    # Devolver estoque
                    for item in pedido.itens.all():
                        item.produto.estoque += item.quantidade
                        item.produto.save()
                    
                    # Cancelar pagamento
                    if hasattr(pedido, 'pagamento'):
                        pedido.pagamento.status = 'cancelado'
                        pedido.pagamento.data_cancelamento = timezone.now()
                        pedido.pagamento.save()
                    
                    # Cancelar pedido
                    pedido.status = 'cancelado'
                    pedido.save()
                    
                    # Adicionar rastreamento
                    RastreamentoEntrega.objects.create(
                        pedido=pedido,
                        status='Pedido Cancelado',
                        descricao='Pedido cancelado pelo cliente.'
                    )
                
                return Response({
                    'message': 'Pedido cancelado com sucesso'
                })


    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def rastreamento_pedido(request, numero_pedido):
                """
                GET /api/pagamento/pedidos/{numero_pedido}/rastreamento/
                Rastreamento do pedido
                """
                pedido = get_object_or_404(
                    Pedido,
                    numero_pedido=numero_pedido,
                    usuario=request.user
                )
                
                rastreamentos = pedido.rastreamentos.all()
                
                return Response({
                    'pedido': numero_pedido,
                    'status_atual': pedido.get_status_display(),
                    'rastreamentos': RastreamentoSerializer(rastreamentos, many=True).data
                })

