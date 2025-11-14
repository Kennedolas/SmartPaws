# ==========================================
# pets/forms.py
# ==========================================

from django import forms
from .models import SolicitacaoAdocao


class SolicitacaoAdocaoForm(forms.ModelForm):
    """Formulário de solicitação de adoção"""
    
    class Meta:
        model = SolicitacaoAdocao
        fields = [
            'nome_completo', 'email', 'telefone', 'endereco',
            'tipo_moradia', 'tem_quintal', 'moradia_propria',
            'tem_outros_pets', 'descricao_outros_pets', 'teve_pets_antes',
            'motivacao'
        ]
        
        widgets = {
            'nome_completo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Seu nome completo'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'seu@email.com'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(00) 00000-0000'
            }),
            'endereco': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Endereço completo'
            }),
            'tipo_moradia': forms.Select(attrs={
                'class': 'form-control'
            }),
            'tem_quintal': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'moradia_propria': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'tem_outros_pets': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'descricao_outros_pets': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Descreva seus outros pets (opcional)'
            }),
            'teve_pets_antes': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'motivacao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Por que você deseja adotar este pet?'
            }),
        }
        
        labels = {
            'nome_completo': 'Nome Completo',
            'email': 'E-mail',
            'telefone': 'Telefone/WhatsApp',
            'endereco': 'Endereço Completo',
            'tipo_moradia': 'Tipo de Moradia',
            'tem_quintal': 'Possui quintal?',
            'moradia_propria': 'É moradia própria?',
            'tem_outros_pets': 'Já tem outros pets?',
            'descricao_outros_pets': 'Descrição dos outros pets',
            'teve_pets_antes': 'Já teve pets antes?',
            'motivacao': 'Por que deseja adotar?',
        }
