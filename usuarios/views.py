# ==========================================
# usuarios/views.py
# ==========================================

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Usuario, Endereco
from .forms import RegistroForm, LoginForm, EnderecoForm


# ========== REGISTRO ==========
def registro_view(request):
    """View de registro de novo usuário"""
    if request.user.is_authenticated:
        return redirect('core:home')
    
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Cadastro realizado com sucesso! Faça login para continuar.')
            return redirect('usuarios:login')
        else:
            messages.error(request, 'Erro no cadastro. Verifique os dados.')
    else:
        form = RegistroForm()
    
    return render(request, 'usuarios/registro.html', {'form': form})


# ========== LOGIN ==========
def login_view(request):
    """View de login"""
    if request.user.is_authenticated:
        return redirect('core:home')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Bem-vindo(a), {user.first_name}!')
                
                # Redireciona para página anterior ou home
                next_page = request.GET.get('next', 'core:home')
                return redirect(next_page)
            else:
                messages.error(request, 'Email ou senha incorretos.')
        else:
            messages.error(request, 'Email ou senha incorretos.')
    else:
        form = LoginForm()
    
    return render(request, 'usuarios/login.html', {'form': form})


# ========== LOGOUT ==========
@login_required
def logout_view(request):
    """View de logout"""
    logout(request)
    messages.success(request, 'Você saiu da sua conta.')
    return redirect('core:home')


# ========== PERFIL ==========
@login_required
def perfil_view(request):
    """View do perfil do usuário"""
    enderecos = request.user.enderecos.all()
    
    context = {
        'user': request.user,
        'enderecos': enderecos,
    }
    
    return render(request, 'usuarios/perfil.html', context)


# ========== EDITAR PERFIL ==========
@login_required
def editar_perfil_view(request):
    """View para editar perfil"""
    if request.method == 'POST':
        user = request.user
        
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.telefone = request.POST.get('telefone', '')
        user.data_nascimento = request.POST.get('data_nascimento', None)
        user.sexo = request.POST.get('sexo', '')
        
        # Upload de foto
        if 'foto_perfil' in request.FILES:
            user.foto_perfil = request.FILES['foto_perfil']
        
        user.save()
        messages.success(request, 'Perfil atualizado com sucesso!')
        return redirect('usuarios:perfil')
    
    return render(request, 'usuarios/editar_perfil.html')


# ========== ENDEREÇOS ==========
@login_required
def adicionar_endereco_view(request):
    """Adicionar novo endereço"""
    if request.method == 'POST':
        form = EnderecoForm(request.POST)
        if form.is_valid():
            endereco = form.save(commit=False)
            endereco.usuario = request.user
            
            # Se for principal, remove outros principais
            if endereco.is_principal:
                request.user.enderecos.filter(is_principal=True).update(is_principal=False)
            
            endereco.save()
            messages.success(request, 'Endereço adicionado com sucesso!')
            return redirect('usuarios:perfil')
    else:
        form = EnderecoForm()
    
    return render(request, 'usuarios/endereco_form.html', {'form': form, 'titulo': 'Adicionar Endereço'})


@login_required
def editar_endereco_view(request, pk):
    """Editar endereço existente"""
    endereco = get_object_or_404(Endereco, pk=pk, usuario=request.user)
    
    if request.method == 'POST':
        form = EnderecoForm(request.POST, instance=endereco)
        if form.is_valid():
            endereco = form.save(commit=False)
            
            if endereco.is_principal:
                request.user.enderecos.filter(is_principal=True).exclude(pk=pk).update(is_principal=False)
            
            endereco.save()
            messages.success(request, 'Endereço atualizado com sucesso!')
            return redirect('usuarios:perfil')
    else:
        form = EnderecoForm(instance=endereco)
    
    return render(request, 'usuarios/endereco_form.html', {'form': form, 'titulo': 'Editar Endereço'})


@login_required
def deletar_endereco_view(request, pk):
    """Deletar endereço"""
    endereco = get_object_or_404(Endereco, pk=pk, usuario=request.user)
    
    if request.method == 'POST':
        endereco.delete()
        messages.success(request, 'Endereço removido com sucesso!')
        return redirect('usuarios:perfil')
    
    return render(request, 'usuarios/endereco_confirm_delete.html', {'endereco': endereco})


# ========== RECUPERAR SENHA ==========
def esqueci_senha_view(request):
    """Solicitar recuperação de senha"""
    if request.method == 'POST':
        email = request.POST.get('email')
        
        try:
            user = Usuario.objects.get(email=email)
            # Aqui você implementaria envio de email
            messages.success(request, 'Instruções de recuperação foram enviadas para seu email.')
            return redirect('usuarios:login')
        except Usuario.DoesNotExist:
            messages.error(request, 'Email não encontrado.')
    
    return render(request, 'usuarios/esqueci_senha.html')
