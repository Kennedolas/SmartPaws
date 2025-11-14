"""
Script para popular o banco de dados - Smart Paws
PETS e SERVIÇOS
"""

import os
import django
import random
from datetime import datetime, timedelta, date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartpaws.settings')
django.setup()

from pets.models import Pet, SolicitacaoAdocao
from servicos.models import CategoriaServico, Prestador, Servico, AgendamentoServico
from usuarios.models import Usuario
from decimal import Decimal

print("\n" + "="*70)
print("🐾 SMART PAWS - POPULAR BANCO DE DADOS")
print("="*70 + "\n")

# ============================================
# DADOS - PETS
# ============================================

PETS_DATA = [
    {'nome': 'Rex', 'especie': 'cao', 'raca': 'Vira-lata', 'idade_anos': 3, 'sexo': 'M', 'porte': 'medio', 'cor': 'Caramelo'},
    {'nome': 'Luna', 'especie': 'gato', 'raca': 'Siamês', 'idade_anos': 2, 'sexo': 'F', 'porte': 'pequeno', 'cor': 'Branco'},
    {'nome': 'Max', 'especie': 'cao', 'raca': 'Labrador', 'idade_anos': 4, 'sexo': 'M', 'porte': 'grande', 'cor': 'Preto'},
    {'nome': 'Bella', 'especie': 'cao', 'raca': 'Poodle', 'idade_anos': 1, 'sexo': 'F', 'porte': 'pequeno', 'cor': 'Branco'},
    {'nome': 'Thor', 'especie': 'cao', 'raca': 'Pastor Alemão', 'idade_anos': 5, 'sexo': 'M', 'porte': 'grande', 'cor': 'Marrom'},
    {'nome': 'Nina', 'especie': 'gato', 'raca': 'Persa', 'idade_anos': 2, 'sexo': 'F', 'porte': 'pequeno', 'cor': 'Cinza'},
    {'nome': 'Bob', 'especie': 'cao', 'raca': 'Bulldog', 'idade_anos': 3, 'sexo': 'M', 'porte': 'medio', 'cor': 'Branco'},
    {'nome': 'Mel', 'especie': 'gato', 'raca': 'Vira-lata', 'idade_anos': 1, 'sexo': 'F', 'porte': 'pequeno', 'cor': 'Tigrado'},
    {'nome': 'Zeus', 'especie': 'cao', 'raca': 'Golden Retriever', 'idade_anos': 6, 'sexo': 'M', 'porte': 'grande', 'cor': 'Dourado'},
    {'nome': 'Lola', 'especie': 'cao', 'raca': 'Yorkshire', 'idade_anos': 2, 'sexo': 'F', 'porte': 'pequeno', 'cor': 'Marrom'},
    {'nome': 'Duke', 'especie': 'cao', 'raca': 'Beagle', 'idade_anos': 3, 'sexo': 'M', 'porte': 'medio', 'cor': 'Tricolor'},
    {'nome': 'Mia', 'especie': 'gato', 'raca': 'Bengal', 'idade_anos': 1, 'sexo': 'F', 'porte': 'pequeno', 'cor': 'Tigrado'},
    {'nome': 'Rocky', 'especie': 'cao', 'raca': 'Rottweiler', 'idade_anos': 4, 'sexo': 'M', 'porte': 'grande', 'cor': 'Preto'},
    {'nome': 'Sophie', 'especie': 'gato', 'raca': 'Maine Coon', 'idade_anos': 3, 'sexo': 'F', 'porte': 'medio', 'cor': 'Cinza'},
    {'nome': 'Charlie', 'especie': 'cao', 'raca': 'Shih Tzu', 'idade_anos': 2, 'sexo': 'M', 'porte': 'pequeno', 'cor': 'Branco'},
]

# ============================================
# DADOS - CATEGORIAS DE SERVIÇOS
# ============================================

CATEGORIAS_DATA = [
    {'nome': 'Banho e Tosa', 'icone': 'fa-shower', 'ordem': 1},
    {'nome': 'Veterinário', 'icone': 'fa-stethoscope', 'ordem': 2},
    {'nome': 'Hospedagem', 'icone': 'fa-hotel', 'ordem': 3},
    {'nome': 'Passeios', 'icone': 'fa-walking', 'ordem': 4},
    {'nome': 'Adestramento', 'icone': 'fa-graduation-cap', 'ordem': 5},
]

# ============================================
# DADOS - PRESTADORES
# ============================================

PRESTADORES_DATA = [
    {
        'nome': 'Pet Care Center',
        'descricao': 'Centro completo de cuidados para seu pet com profissionais qualificados.',
        'telefone': '(11) 98765-4321',
        'email': 'contato@petcare.com',
        'endereco': 'Rua das Flores, 123',
        'bairro': 'Centro',
        'cidade': 'São Paulo',
        'estado': 'SP',
        'avaliacao_media': Decimal('4.8'),
        'verificado': True
    },
    {
        'nome': 'Clínica Veterinária PetHealth',
        'descricao': 'Clínica veterinária com atendimento 24h e equipamentos modernos.',
        'telefone': '(11) 91234-5678',
        'email': 'contato@pethealth.com',
        'endereco': 'Av. Paulista, 500',
        'bairro': 'Bela Vista',
        'cidade': 'São Paulo',
        'estado': 'SP',
        'avaliacao_media': Decimal('4.9'),
        'verificado': True
    },
]

# ============================================
# FUNÇÕES
# ============================================

def criar_pets():
    print("🐾 Criando pets para adoção...\n")
    criados = 0
    
    descricoes = [
        'Pet muito carinhoso e brincalhão, ótimo para famílias.',
        'Animal calmo e sociável, se dá bem com outros pets.',
        'Cheio de energia, perfeito para atividades ao ar livre.',
        'Dócil e protetor, ideal para apartamentos.',
        'Adora brincar e fazer companhia, muito inteligente.',
    ]
    
    temperamentos = ['Calmo', 'Brincalhão', 'Protetor', 'Sociável', 'Energético']
    
    for pet_data in PETS_DATA:
        pet, created = Pet.objects.get_or_create(
            nome=pet_data['nome'],
            defaults={
                'especie': pet_data['especie'],
                'raca': pet_data['raca'],
                'idade_anos': pet_data['idade_anos'],
                'idade_meses': 0,
                'porte': pet_data['porte'],
                'sexo': pet_data['sexo'],
                'cor': pet_data['cor'],
                'castrado': random.choice([True, False]),
                'vacinado': random.choice([True, True, False]),
                'vermifugado': random.choice([True, False]),
                'descricao': random.choice(descricoes),
                'temperamento': random.choice(temperamentos),
                'status': 'disponivel',
            }
        )
        
        if created:
            criados += 1
            castrado = '✂️' if pet.castrado else ''
            vacinado = '💉' if pet.vacinado else ''
            print(f"  ✅ {pet.nome:12} - {pet.get_especie_display():10} {pet.raca:20} {castrado} {vacinado}")
    
    print(f"\n✨ Total de pets criados: {criados}\n")
    return criados

def criar_categorias():
    print("📂 Criando categorias de serviços...\n")
    criados = 0
    
    for cat_data in CATEGORIAS_DATA:
        cat, created = CategoriaServico.objects.get_or_create(
            nome=cat_data['nome'],
            defaults={
                'icone': cat_data['icone'],
                'ordem': cat_data['ordem'],
                'ativo': True
            }
        )
        
        if created:
            criados += 1
            print(f"  ✅ {cat.nome}")
    
    print(f"\n✨ Total de categorias criadas: {criados}\n")
    return criados

def criar_prestadores():
    print("🏢 Criando prestadores de serviços...\n")
    criados = 0
    
    for prest_data in PRESTADORES_DATA:
        prest, created = Prestador.objects.get_or_create(
            nome=prest_data['nome'],
            defaults={
                'descricao': prest_data['descricao'],
                'telefone': prest_data['telefone'],
                'email': prest_data['email'],
                'endereco': prest_data['endereco'],
                'bairro': prest_data['bairro'],
                'cidade': prest_data['cidade'],
                'estado': prest_data['estado'],
                'avaliacao_media': prest_data['avaliacao_media'],
                'total_avaliacoes': random.randint(10, 50),
                'verificado': prest_data['verificado'],
                'ativo': True,
                'destaque': True
            }
        )
        
        if created:
            criados += 1
            print(f"  ✅ {prest.nome} - ⭐ {prest.avaliacao_media}")
    
    print(f"\n✨ Total de prestadores criados: {criados}\n")
    return criados

def criar_servicos():
    print("💼 Criando serviços...\n")
    
    prestadores = list(Prestador.objects.filter(ativo=True))
    categorias = list(CategoriaServico.objects.filter(ativo=True))
    
    if not prestadores:
        print("  ⚠️ Nenhum prestador encontrado!\n")
        return 0
    
    servicos_data = [
        {'nome': 'Banho e Tosa Completo', 'categoria': 'Banho e Tosa', 'preco': '80.00', 'duracao': '2 horas'},
        {'nome': 'Banho Básico', 'categoria': 'Banho e Tosa', 'preco': '50.00', 'duracao': '1 hora'},
        {'nome': 'Tosa Higiênica', 'categoria': 'Banho e Tosa', 'preco': '40.00', 'duracao': '45 minutos'},
        {'nome': 'Consulta Veterinária', 'categoria': 'Veterinário', 'preco': '200.00', 'duracao': '45 minutos'},
        {'nome': 'Vacinação V10', 'categoria': 'Veterinário', 'preco': '150.00', 'duracao': '15 minutos'},
        {'nome': 'Vacinação Antirrábica', 'categoria': 'Veterinário', 'preco': '80.00', 'duracao': '15 minutos'},
        {'nome': 'Hotel Pet - Diária', 'categoria': 'Hospedagem', 'preco': '150.00', 'duracao': '24 horas'},
        {'nome': 'Creche Pet Diária', 'categoria': 'Hospedagem', 'preco': '120.00', 'duracao': '8 horas'},
        {'nome': 'Dog Walker - 30min', 'categoria': 'Passeios', 'preco': '35.00', 'duracao': '30 minutos'},
        {'nome': 'Dog Walker - 1 hora', 'categoria': 'Passeios', 'preco': '60.00', 'duracao': '1 hora'},
        {'nome': 'Adestramento Básico', 'categoria': 'Adestramento', 'preco': '300.00', 'duracao': '1 hora'},
        {'nome': 'Adestramento Avançado', 'categoria': 'Adestramento', 'preco': '500.00', 'duracao': '1.5 horas'},
    ]
    
    criados = 0
    
    for serv_data in servicos_data:
        prestador = random.choice(prestadores)
        categoria = next((c for c in categorias if c.nome == serv_data['categoria']), None)
        
        servico, created = Servico.objects.get_or_create(
            nome=serv_data['nome'],
            prestador=prestador,
            defaults={
                'categoria': categoria,
                'descricao': f"{serv_data['nome']} - Serviço de qualidade com profissionais experientes.",
                'descricao_curta': f"{serv_data['nome']} - {serv_data['duracao']}",
                'preco': Decimal(serv_data['preco']),
                'duracao': serv_data['duracao'],
                'ativo': True,
                'destaque': random.choice([True, False, False])
            }
        )
        
        if created:
            criados += 1
            destaque = '⭐' if servico.destaque else ''
            print(f"  ✅ {servico.nome:30} R$ {str(servico.preco):8} {destaque}")
    
    print(f"\n✨ Total de serviços criados: {criados}\n")
    return criados

def criar_agendamentos():
    print("📅 Criando agendamentos de exemplo...\n")
    
    usuarios = list(Usuario.objects.filter(is_active=True))
    servicos = list(Servico.objects.filter(ativo=True))
    
    if not usuarios or not servicos:
        print("  ⚠️ Nenhum usuário ou serviço encontrado!\n")
        return 0
    
    criados = 0
    nomes_pets = ['Rex', 'Luna', 'Max', 'Bella', 'Thor', 'Nina', 'Bob']
    
    for i in range(10):
        usuario = random.choice(usuarios)
        servico = random.choice(servicos)
        
        dias = random.randint(1, 30)
        data_agendamento = date.today() + timedelta(days=dias)
        horario = datetime.strptime(f"{random.randint(8, 17)}:00", "%H:%M").time()
        
        agendamento, created = AgendamentoServico.objects.get_or_create(
            usuario=usuario,
            servico=servico,
            data_agendamento=data_agendamento,
            horario=horario,
            defaults={
                'nome_pet': random.choice(nomes_pets),
                'status': random.choice(['pendente', 'confirmado']),
                'observacoes': 'Agendamento de teste'
            }
        )
        
        if created:
            criados += 1
            print(f"  ✅ {usuario.email[:25]:25} - {servico.nome[:25]:25} - {data_agendamento}")
    
    print(f"\n✨ Total de agendamentos criados: {criados}\n")
    return criados

# ============================================
# EXECUÇÃO
# ============================================

try:
    pets = criar_pets()
    categorias = criar_categorias()
    prestadores = criar_prestadores()
    servicos = criar_servicos()
    agendamentos = criar_agendamentos()
    
    print("="*70)
    print("✅ RESUMO FINAL:")
    print(f"   🐾 Pets: {pets}")
    print(f"   📂 Categorias: {categorias}")
    print(f"   🏢 Prestadores: {prestadores}")
    print(f"   💼 Serviços: {servicos}")
    print(f"   📅 Agendamentos: {agendamentos}")
    print("="*70)
    print("\n✨ Banco de dados populado com sucesso! 🎉\n")
    
except Exception as e:
    print(f"\n❌ ERRO: {e}\n")
    import traceback
    traceback.print_exc()
