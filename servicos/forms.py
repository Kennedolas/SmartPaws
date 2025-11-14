# ==========================================
# servicos/forms.py
# ==========================================

from django import forms
from .models import AgendamentoServico


class AgendamentoServicoForm(forms.ModelForm):
    """Formulário de agendamento de serviço"""
    
    class Meta:
        model = AgendamentoServico
        fields = ['data_agendamento', 'horario', 'nome_pet', 'observacoes']
        
        widgets = {
            'data_agendamento': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
            }),
            'horario': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control',
            }),
            'nome_pet': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do seu pet',
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Informações adicionais que o prestador deve saber...',
            }),
        }
        
        labels = {
            'data_agendamento': 'Data do Agendamento',
            'horario': 'Horário Preferido',
            'nome_pet': 'Nome do Pet',
            'observacoes': 'Observações',
        }
