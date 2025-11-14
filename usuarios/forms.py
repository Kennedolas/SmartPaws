# ==========================================
# usuarios/forms.py
# ==========================================

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario, Endereco


class RegistroForm(UserCreationForm):
    """Formulário de registro de usuário"""
    
    first_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Digite seu nome',
            'class': 'nome'
        })
    )
    
    last_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Digite seu sobrenome',
            'class': 'nome'
        })
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'DIGITE O SEU EMAIL',
            'class': 'email'
        })
    )
    
    cpf = forms.CharField(
        max_length=14,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'DIGITE O SEU CPF',
            'class': 'cpf',
            'maxlength': '14'
        })
    )
    
    telefone = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'DDD + CELULAR',
            'class': 'celular'
        })
    )
    
    data_nascimento = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'data'
        })
    )
    
    sexo = forms.ChoiceField(
        choices=[('', 'Selecione')] + Usuario.SEXO_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'sexo'})
    )
    
    password1 = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'DIGITE SUA SENHA',
            'class': 'senha',
            'minlength': '8'
        })
    )
    
    password2 = forms.CharField(
        label="Confirmar Senha",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'CONFIRME SUA SENHA',
            'class': 'confirmarsenha',
            'minlength': '8'
        })
    )
    
    aceita_marketing = forms.BooleanField(
        required=False,
        label='Aceito receber ofertas e novidades'
    )
    
    class Meta:
        model = Usuario
        fields = [
            'first_name', 'last_name', 'email', 'cpf', 'telefone',
            'data_nascimento', 'sexo', 'password1', 'password2', 'aceita_marketing'
        ]
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email'].lower()
        
        if commit:
            user.save()
            user.generate_verification_token()
        
        return user


class LoginForm(AuthenticationForm):
    """Formulário de login"""
    
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'DIGITE O SEU EMAIL',
            'class': 'email',
            'id': 'email'
        })
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'DIGITE A SUA SENHA',
            'class': 'senha',
            'id': 'senha'
        })
    )


class EnderecoForm(forms.ModelForm):
    """Formulário de endereço"""
    
    class Meta:
        model = Endereco
        fields = [
            'nome', 'cep', 'logradouro', 'numero', 'complemento',
            'bairro', 'cidade', 'estado', 'is_principal'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Ex: Casa, Trabalho'}),
            'cep': forms.TextInput(attrs={'placeholder': '00000-000'}),
            'logradouro': forms.TextInput(attrs={'placeholder': 'Rua, Avenida...'}),
            'numero': forms.TextInput(attrs={'placeholder': 'Número'}),
            'complemento': forms.TextInput(attrs={'placeholder': 'Apto, Bloco...'}),
            'bairro': forms.TextInput(attrs={'placeholder': 'Bairro'}),
            'cidade': forms.TextInput(attrs={'placeholder': 'Cidade'}),
        }
