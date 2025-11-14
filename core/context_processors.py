def site_info(request):
    """Informações globais do site disponíveis em todos os templates"""
    return {
        'site_name': 'Smart Paws',
        'site_description': 'Descricao',
        'ano_atual': 2025,
        
        # Links de redes sociais
        'social_facebook': '#', #botar
        'social_instagram': '#',#botar
        'social_twitter': '#',#botar
    }
