from django import forms
from .models import SolicitacaoAdocao, PromocaoAdocao


class SolicitacaoAdocaoForm(forms.ModelForm):
    class Meta:
        model = SolicitacaoAdocao
        fields = [
            'nome_completo', 'email', 'telefone', 'cpf',
            'endereco', 'cidade', 'estado', 'cep',
            'tipo_moradia', 'possui_quintal', 'tem_outros_pets', 
            'descricao_outros_pets', 'motivo_adocao', 'experiencia_pets'
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
            'cpf': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '000.000.000-00'
            }),
            'endereco': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Rua, número, complemento'
            }),
            'cidade': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sua cidade'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-control'
            }),
            'cep': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '00000-000'
            }),
            'tipo_moradia': forms.Select(attrs={
                'class': 'form-control'
            }),
            'possui_quintal': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'tem_outros_pets': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'descricao_outros_pets': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descreva seus outros pets (se houver)'
            }),
            'motivo_adocao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Por que você quer adotar este pet?'
            }),
            'experiencia_pets': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Conte sobre sua experiência com pets'
            }),
        }
        
        labels = {
            'nome_completo': 'Nome Completo',
            'email': 'E-mail',
            'telefone': 'Telefone',
            'cpf': 'CPF',
            'endereco': 'Endereço',
            'cidade': 'Cidade',
            'estado': 'Estado',
            'cep': 'CEP',
            'tipo_moradia': 'Tipo de Moradia',
            'possui_quintal': 'Possui quintal?',
            'tem_outros_pets': 'Tem outros pets?',
            'descricao_outros_pets': 'Descrição dos outros pets',
            'motivo_adocao': 'Por que você quer adotar?',
            'experiencia_pets': 'Experiência com pets',
        }


class PromocaoAdocaoForm(forms.ModelForm):
    class Meta:
        model = PromocaoAdocao
        fields = [
            'nome_pet', 'tipo_pet', 'sexo', 'idade', 'raca', 
            'descricao', 'foto', 'nome_responsavel', 'email', 
            'telefone', 'cidade', 'estado', 'motivo', 
            'castrado', 'vacinado'
        ]
        
        widgets = {
            'nome_pet': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do pet'
            }),
            'tipo_pet': forms.Select(attrs={
                'class': 'form-control'
            }),
            'sexo': forms.Select(attrs={
                'class': 'form-control'
            }),
            'idade': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Idade em meses',
                'min': 0
            }),
            'raca': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Raça (ou "SRD" para sem raça definida)'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descreva o pet, seu temperamento, características...'
            }),
            'foto': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'nome_responsavel': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Seu nome'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'seu@email.com'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(00) 00000-0000'
            }),
            'cidade': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cidade onde o pet está'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-control'
            }),
            'motivo': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Por que está promovendo a adoção deste pet?'
            }),
            'castrado': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'vacinado': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        
        labels = {
            'nome_pet': 'Nome do Pet',
            'tipo_pet': 'Tipo',
            'sexo': 'Sexo',
            'idade': 'Idade (meses)',
            'raca': 'Raça',
            'descricao': 'Descrição',
            'foto': 'Foto do Pet',
            'nome_responsavel': 'Seu Nome',
            'email': 'Seu E-mail',
            'telefone': 'Seu Telefone',
            'cidade': 'Cidade',
            'estado': 'Estado',
            'motivo': 'Motivo da Adoção',
            'castrado': 'O pet é castrado?',
            'vacinado': 'O pet está vacinado?',
        }
