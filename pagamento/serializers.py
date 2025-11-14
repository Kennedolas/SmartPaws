from rest_framework import serializers
from .models import Endereco, Pagamentos, RastreamentoEntrega, Pedido, ItemPedido

class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = '__all__'
        read_only_fields = ['usuario', 'data_cadastro']


class ItemPedidoSerializer(serializers.ModelSerializer):
    produto_nome = serializers.CharField(source='nome_produto', read_only=True)
    loja_nome = serializers.CharField(source='loja.nome', read_only=True)

    class Meta:
        
        model = ItemPedido
        fields = ['id', 'produto', 'produto_nome', 'loja', 'loja_nome',
            'preco_unitario', 'quantidade', 'subtotal']
        read_only_fields = ['subtotal']


class PagamentoSerializer(serializers.ModelSerializer):

    forma_pagamento_display = serializers.CharField(
        source='get_forma_pagamento_display',
        read_only=True
    )
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )
    
    class Meta:
        model = Pagamentos
        fields = [
            'id', 'forma_pagamento', 'forma_pagamento_display',
            'valor', 'status', 'status_display',
            'bandeira_cartao', 'ultimos_digitos',
            'chave_pix', 'qr_code_pix',
            'codigo_boleto', 'link_boleto',
            'data_criacao', 'data_aprovacao', 'mensagem_erro'
        ]
        read_only_fields = [
            'data_criacao', 'data_aprovacao', 'qr_code_pix',
            'codigo_boleto', 'link_boleto'
        ]


class RastreamentoSerializer:
    
    class Meta:
        model = RastreamentoEntrega
        fields = ['id', 'status,' 'descricao,', 'localizacao']
        ready_only_fields = ['data_hora']



class PedidoSerializer(serializers.ModelSerializer):

    itens = ItemPedidoSerializer(many=True, read_only=True)
    pagamento = PagamentoSerializer(read_only=True)
    rastreamentos = RastreamentoSerializer(many=True, read_only=True)
    endereco_entrega_detalhes = EnderecoSerializer(source='endereco_entrega', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    total_itens = serializers.IntegerField(read_only=True)
    pode_cancelar = serializers.BooleanField(read_only=True)

    class Meta:
        model = Pedido
        fields = ['numero_pedido', 'uuid', 'usuario', 'subtotal', 'total',
            'data_pedido', 'data_pagamento', 'data_envio', 'data_entrega']
