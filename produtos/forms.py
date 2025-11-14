# ==========================================
# produtos/forms.py
# ==========================================

from django import forms
from .models import CategoriaProduto


class ProdutoFiltroForm(forms.Form):
    """Formulário de busca e filtro de produtos"""
    
    busca = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Buscar produtos...',
            'class': 'barra_pesquisa'
        })
    )
    
    categoria = forms.ModelChoiceField(
        queryset=CategoriaProduto.objects.filter(ativo=True),
        required=False,
        empty_label="Todas as categorias",
        widget=forms.Select(attrs={'class': 'select-categoria'})
    )
    
    preco_min = forms.DecimalField(
        required=False,
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'placeholder': 'R$ Min',
            'class': 'input-preco',
            'step': '0.01'
        })
    )
    
    preco_max = forms.DecimalField(
        required=False,
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'placeholder': 'R$ Max',
            'class': 'input-preco',
            'step': '0.01'
        })
    )
    
    ordenar_por = forms.ChoiceField(
        choices=[
            ('', 'Ordenar por'),
            ('nome', 'Nome (A-Z)'),
            ('-nome', 'Nome (Z-A)'),
            ('preco_original', 'Menor preço'),
            ('-preco_original', 'Maior preço'),
            ('-created_at', 'Mais recentes'),
            ('-avaliacao', 'Melhor avaliação'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'select-ordenacao'})
    )


class AdicionarCarrinhoForm(forms.Form):
    """Formulário para adicionar produto ao carrinho"""
    
    produto_id = forms.IntegerField(widget=forms.HiddenInput())
    
    quantidade = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'quantidade-input',
            'min': '1',
            'value': '1'
        })
    )
    
    def __init__(self, *args, produto=None, **kwargs):
        super().__init__(*args, **kwargs)
        if produto:
            # Limita quantidade máxima ao estoque disponível
            self.fields['quantidade'].widget.attrs['max'] = produto.estoque
            self.fields['quantidade'].validators.append(
                forms.validators.MaxValueValidator(produto.estoque)
            )


class AvaliacaoProdutoForm(forms.Form):
    """Formulário para avaliar produtos"""
    
    nota = forms.IntegerField(
        min_value=1,
        max_value=5,
        widget=forms.RadioSelect(
            choices=[(i, f'{i}') for i in range(1, 6)],
            attrs={'class': 'rating-stars'}
        )
    )
    
    titulo = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Título da avaliação',
            'class': 'form-control'
        })
    )
    
    comentario = forms.CharField(
        max_length=1000,
        widget=forms.Textarea(attrs={
            'placeholder': 'Conte sua experiência com o produto...',
            'class': 'form-control',
            'rows': 4
        })
    )
    
    nome = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Seu nome',
            'class': 'form-control'
        })
    )
    
    recomenda = forms.BooleanField(
        required=False,
        initial=True,
        label='Eu recomendo este produto'
    )


class NotificarDisponibilidadeForm(forms.Form):
    """Formulário para avisar quando produto voltar ao estoque"""
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Digite seu e-mail',
            'class': 'form-control'
        })
    )
    
    produto_id = forms.IntegerField(widget=forms.HiddenInput())
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Validação adicional se necessário
        return email.lower()
