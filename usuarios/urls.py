# ==========================================
# usuarios/urls.py
# ==========================================

from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    # Autenticação
    path('registro/', views.registro_view, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('esqueci-senha/', views.esqueci_senha_view, name='esqueci_senha'),
    
    # Perfil
    path('perfil/', views.perfil_view, name='perfil'),
    path('perfil/editar/', views.editar_perfil_view, name='editar_perfil'),
    
    # Endereços
    path('endereco/adicionar/', views.adicionar_endereco_view, name='adicionar_endereco'),
    path('endereco/<int:pk>/editar/', views.editar_endereco_view, name='editar_endereco'),
    path('endereco/<int:pk>/deletar/', views.deletar_endereco_view, name='deletar_endereco'),
]
