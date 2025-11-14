from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils import timezone
from .models import Usuario, Endereco
import re
from datetime import date

class EnderecoSerializer(serializers.ModelSerializer):

    
    endereco_completo = serializers.ReadOnlyField()
    
    class Meta:
        model = Endereco
        fields = [
            'id', 'nome', 'cep', 'logradouro', 'numero', 
            'complemento', 'bairro', 'cidade', 'estado',
            'is_principal', 'endereco_completo', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def validate_cep(self, value):

        cep_pattern = re.compile(r'^\d{5}-?\d{3}$')
        if not cep_pattern.match(value):
            raise serializers.ValidationError("CEP deve estar no formato: 00000-000")
        return value


class UsuarioBasicoSerializer(serializers.ModelSerializer):

    
    nome_completo = serializers.ReadOnlyField()
    idade = serializers.ReadOnlyField()
    
    class Meta:
        model = Usuario
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'nome_completo', 'idade', 'foto_perfil', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class UsuarioCompletoSerializer(serializers.ModelSerializer):

    
    nome_completo = serializers.ReadOnlyField()
    idade = serializers.ReadOnlyField()
    cpf_formatado = serializers.ReadOnlyField()
    enderecos = EnderecoSerializer(many=True, read_only=True)
    
    class Meta:
        model = Usuario
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'cpf', 'cpf_formatado', 'telefone', 'data_nascimento', 'sexo',
            'foto_perfil', 'is_verified', 'aceita_marketing',
            'nome_completo', 'idade', 'enderecos', 'created_at', 'last_login'
        ]
        read_only_fields = ['id', 'is_verified', 'created_at', 'last_login']


class RegistroSerializer(serializers.ModelSerializer):
  
    
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'},
        help_text="Mínimo 8 caracteres"
    )
    password_confirmation = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = Usuario
        fields = [
            'username', 'email', 'password', 'password_confirmation',
            'first_name', 'last_name', 'cpf', 'telefone',
            'data_nascimento', 'sexo', 'aceita_marketing'
        ]
    
    def validate_email(self, value):
        
        value = value.lower()
        if Usuario.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este email já está em uso.")
        return value
    
    def validate_username(self, value):

        if Usuario.objects.filter(username=value).exists():
            raise serializers.ValidationError("Este nome de usuário já está em uso.")
    
        if not re.match(r'^[a-zA-Z0-9_]+$', value):
            raise serializers.ValidationError("Username deve conter apenas letras, números e underscore.")
        
        return value
    
    def validate_cpf(self, value):
        """Valida CPF único se fornecido"""
        if value:
            cpf_numeros = re.sub(r'[^0-9]', '', value)
            if Usuario.objects.filter(cpf__icontains=cpf_numeros).exists():
                raise serializers.ValidationError("Este CPF já está cadastrado.")
        return value
    
    def validate_data_nascimento(self, value):
        """Valida idade mínima"""
        if value:
            today = date.today()
            idade = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
            if idade < 13:
                raise serializers.ValidationError("Usuário deve ter pelo menos 13 anos.")
            if idade > 120:
                raise serializers.ValidationError("Data de nascimento inválida.")
        return value
    
    def validate_password(self, value):

        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value
    
    def validate(self, attrs):

        if attrs['password'] != attrs['password_confirmation']:
            raise serializers.ValidationError({
                'password_confirmation': 'As senhas não coincidem.'
            })
        
        # Remove confirmação da senha
        attrs.pop('password_confirmation')
        
        return attrs
    
    def create(self, validated_data):
        """Cria novo usuário"""
        password = validated_data.pop('password')
        
        # Criar usuário
        usuario = Usuario.objects.create_user(
            password=password,
            **validated_data
        )
        
        # Gerar token de verificação
        usuario.generate_verification_token()
        
        return usuario


class LoginSerializer(serializers.Serializer):
    """Serializer para autenticação"""
    
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )
    
    def validate(self, attrs):
        """Valida credenciais de login"""
        email = attrs.get('email', '').lower()
        password = attrs.get('password')
        
        if email and password:
            # Tentar autenticar
            user = authenticate(
                request=self.context.get('request'),
                username=email,
                password=password
            )
            
            if not user:
                raise serializers.ValidationError(
                    'Email ou senha incorretos.',
                    code='authorization'
                )
            
            if not user.is_active:
                raise serializers.ValidationError(
                    'Conta de usuário desativada.',
                    code='authorization'
                )
            
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError(
                'Email e senha são obrigatórios.',
                code='authorization'
            )


class PerfilUpdateSerializer(serializers.ModelSerializer):
    """Serializer para atualização de perfil"""
    
    current_password = serializers.CharField(
        write_only=True,
        required=False,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        write_only=True,
        required=False,
        min_length=8,
        style={'input_type': 'password'}
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=False,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = Usuario
        fields = [
            'username', 'first_name', 'last_name', 'cpf', 'telefone',
            'data_nascimento', 'sexo', 'aceita_marketing',
            'current_password', 'new_password', 'confirm_password'
        ]
    
    def validate_username(self, value):
        
        if Usuario.objects.filter(username=value).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError("Este nome de usuário já está em uso.")
        return value
    
    def validate_cpf(self, value):
        if value:
            cpf_numeros = re.sub(r'[^0-9]', '', value)
            if Usuario.objects.filter(cpf__icontains=cpf_numeros).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("Este CPF já está cadastrado.")
        return value
    
    def validate_data_nascimento(self, value):

        if value:
            today = date.today()
            idade = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
            if idade < 13:
                raise serializers.ValidationError("Usuário deve ter pelo menos 13 anos.")
        return value
    
    def validate(self, attrs):

        current_password = attrs.get('current_password')
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')
        
        # Se forneceu nova senha, validar processo completo
        if any([current_password, new_password, confirm_password]):
            if not all([current_password, new_password, confirm_password]):
                raise serializers.ValidationError(
                    'Para alterar senha, forneça: senha atual, nova senha e confirmação.'
                )
            
            # Verificar senha atual
            if not self.instance.check_password(current_password):
                raise serializers.ValidationError({
                    'current_password': 'Senha atual incorreta.'
                })
            
       
            if new_password != confirm_password:
                raise serializers.ValidationError({
                    'confirm_password': 'As senhas não coincidem.'
                })
 
            try:
                validate_password(new_password, self.instance)
            except DjangoValidationError as e:
                raise serializers.ValidationError({
                    'new_password': list(e.messages)
                })
       
        for field in ['current_password', 'new_password', 'confirm_password']:
            attrs.pop(field, None)
        
        return attrs
    
    def update(self, instance, validated_data):
  
        new_password = self.initial_data.get('new_password')
        
      
        for field, value in validated_data.items():
            setattr(instance, field, value)
        

        if new_password:
            instance.set_password(new_password)
        
        instance.save()
        return instance


class AlterarSenhaSerializer(serializers.Serializer):

    
    current_password = serializers.CharField(style={'input_type': 'password'})
    new_password = serializers.CharField(min_length=8, style={'input_type': 'password'})
    confirm_password = serializers.CharField(style={'input_type': 'password'})
    
    def validate_current_password(self, value):
        
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Senha atual incorreta.')
        return value
    
    def validate_new_password(self, value):
  
        try:
            validate_password(value, self.context['request'].user)
        except DjangoValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value
    
    def validate(self, attrs):
  
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({
                'confirm_password': 'As senhas não coincidem.'
            })
        return attrs
    
    def save(self):

        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class VerificacaoEmailSerializer(serializers.Serializer):

    
    token = serializers.CharField()
    
    def validate_token(self, value):
      
        try:
            user = Usuario.objects.get(verification_token=value, is_active=True)
            return value
        except Usuario.DoesNotExist:
            raise serializers.ValidationError('Token de verificação inválido ou expirado.')
    
    def save(self):

        token = self.validated_data['token']
        user = Usuario.objects.get(verification_token=token)
        user.verify_email()
        return user


class ResetSenhaRequestSerializer(serializers.Serializer):

    
    email = serializers.EmailField()
    
    def validate_email(self, value):
      
        value = value.lower()
        if not Usuario.objects.filter(email=value, is_active=True).exists():
            raise serializers.ValidationError('Email não encontrado.')
        return value


class ResetSenhaConfirmSerializer(serializers.Serializer):

    
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=8, style={'input_type': 'password'})
    confirm_password = serializers.CharField(style={'input_type': 'password'})
    
    def validate_token(self, value):
        
        try:
            user = Usuario.objects.get(reset_password_token=value, is_active=True)
            return value
        except Usuario.DoesNotExist:
            raise serializers.ValidationError('Token de reset inválido ou expirado.')
    
    def validate_new_password(self, value):
 
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value
    
    def validate(self, attrs):
  
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({
                'confirm_password': 'As senhas não coincidem.'
            })
        return attrs
    
    def save(self):
     
        token = self.validated_data['token']
        new_password = self.validated_data['new_password']
        
        user = Usuario.objects.get(reset_password_token=token)
        user.set_password(new_password)
        user.reset_password_token = None
        user.save()
        return user