from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Min, Max
from .models import Produto, Categoria, Marca, Avaliacao
from django import forms
from django.core.validators import validate_email
import re

class ContatoForm(forms.Form):
    """Formulário de contato"""
    
    nome = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Seu nome completo',
            'required': True
        }),
        label='Nome Completo'
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'seu@email.com',
            'required': True
        }),
        label='Email'
    )
    
    telefone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '(11) 91234-5678',
            'data-mask': '(00) 00000-0000'
        }),
        label='Telefone (opcional)'
    )
    
    ASSUNTOS_CHOICES = [
        ('duvida', 'Dúvida sobre produtos'),
        ('adocao', 'Adoção de pets'),
        ('servicos', 'Serviços veterinários'),
        ('reclamacao', 'Reclamação'),
        ('sugestao', 'Sugestão'),
        ('outro', 'Outro'),
    ]
    
    assunto = forms.ChoiceField(
        choices=ASSUNTOS_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'required': True
        }),
        label='Assunto'
    )
    
    mensagem = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Escreva sua mensagem aqui...',
            'required': True
        }),
        label='Mensagem'
    )
    
    def clean_nome(self):
        """Valida nome"""
        nome = self.cleaned_data.get('nome', '').strip()
        
        if len(nome) < 2:
            raise forms.ValidationError('Nome deve ter pelo menos 2 caracteres.')
        
        # Verificar se contém apenas letras e espaços
        if not re.match(r'^[a-zA-ZÀ-ÿ\s]+$', nome):
            raise forms.ValidationError('Nome deve conter apenas letras.')
        
        return nome
    
    def clean_telefone(self):
        """Valida telefone se fornecido"""
        telefone = self.cleaned_data.get('telefone', '').strip()
        
        if telefone:
            # Remove formatação
            telefone_numeros = re.sub(r'[^0-9]', '', telefone)
            
            # Verifica se tem 10 ou 11 dígitos
            if len(telefone_numeros) not in [10, 11]:
                raise forms.ValidationError('Telefone deve ter 10 ou 11 dígitos.')
        
        return telefone
    
    def clean_mensagem(self):
        """Valida mensagem"""
        mensagem = self.cleaned_data.get('mensagem', '').strip()
        
        if len(mensagem) < 10:
            raise forms.ValidationError('Mensagem deve ter pelo menos 10 caracteres.')
        
        if len(mensagem) > 1000:
            raise forms.ValidationError('Mensagem deve ter no máximo 1000 caracteres.')
        
        return mensagem


class NewsletterForm(forms.Form):
    """Formulário de inscrição na newsletter"""
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Seu email para receber ofertas',
            'required': True
        }),
        label='Email'
    )
    
    aceito_termos = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='Aceito receber emails promocionais'
    )
    
    def clean_email(self):
        """Valida email"""
        email = self.cleaned_data.get('email', '').strip().lower()
        
        try:
            validate_email(email)
        except forms.ValidationError:
            raise forms.ValidationError('Email inválido.')
        
        return email


class BuscaForm(forms.Form):
    """Formulário de busca geral"""
    
    q = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar produtos, pets...',
            'autocomplete': 'off'
        }),
        label='Buscar'
    )
    
    def clean_q(self):
        """Valida termo de busca"""
        busca = self.cleaned_data.get('q', '').strip()
        
        if busca and len(busca) < 2:
            raise forms.ValidationError('Digite pelo menos 2 caracteres.')
        
        return busca