import django_filters
from django.db.models import Q
from .models import Profissional, Servico, TipoServico


class ProfissionalFilter(django_filters.FilterSet):

    
    cidade = django_filters.CharFilter(
        field_name='cidade',
        lookup_expr='icontains',
        label='Cidade'
    )
    
    estado = django_filters.CharFilter(
        field_name='estado',
        label='Estado'
    )
    
    tipo_servico = django_filters.ModelChoiceFilter(
        queryset=TipoServico.objects.filter(ativo=True),
        field_name='servicos__tipo_servico',
        distinct=True,
        label='Tipo de Serviço'
    )
    
    aceita_emergencia = django_filters.BooleanFilter(
        field_name='aceita_emergencia',
        label='Aceita Emergências'
    )
    
    trabalha_finais_semana = django_filters.BooleanFilter(
        field_name='trabalha_finais_semana',
        label='Trabalha Finais de Semana'
    )
    
    nota_minima = django_filters.NumberFilter(
        field_name='nota_media',
        lookup_expr='gte',
        label='Nota Mínima'
    )
    
    verificado = django_filters.BooleanFilter(
        field_name='verificado',
        label='Apenas Verificados'
    )
    
    preco_max = django_filters.NumberFilter(
        field_name='servicos__preco',
        lookup_expr='lte',
        distinct=True,
        label='Preço Máximo'
    )
    
    class Meta:
        model = Profissional
        fields = [
            'cidade', 'estado', 'tipo_servico', 'aceita_emergencia',
            'trabalha_finais_semana', 'nota_minima', 'verificado', 'preco_max'
        ]


class ServicoFilter(django_filters.FilterSet):

    
    tipo_servico = django_filters.ModelChoiceFilter(
        queryset=TipoServico.objects.filter(ativo=True),
        label='Tipo de Serviço'
    )
    
    preco_min = django_filters.NumberFilter(
        field_name='preco',
        lookup_expr='gte',
        label='Preço Mínimo'
    )
    
    preco_max = django_filters.NumberFilter(
        field_name='preco',
        lookup_expr='lte',
        label='Preço Máximo'
    )
    
    duracao_max = django_filters.NumberFilter(
        field_name='duracao_minutos',
        lookup_expr='lte',
        label='Duração Máxima (min)'
    )
    
    cidade = django_filters.CharFilter(
        field_name='profissional__cidade',
        lookup_expr='icontains',
        label='Cidade'
    )
    
    aceita_emergencia = django_filters.BooleanFilter(
        field_name='profissional__aceita_emergencia',
        label='Aceita Emergências'
    )
    
    class Meta:
        model = Servico
        fields = [
            'tipo_servico', 'preco_min', 'preco_max', 'duracao_max',
            'cidade', 'aceita_emergencia'
        ]