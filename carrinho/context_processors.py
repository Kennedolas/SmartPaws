def carrinho_context(request):
    """Adiciona informações do carrinho em todos os templates"""
    if request.user.is_authenticated:
        from .models import Carrinho
        carrinho, _ = Carrinho.objects.get_or_create(usuario=request.user)
        return {
            'carrinho_total_itens': carrinho.total_itens,
        }
    return {
        'carrinho_total_itens': 0,
    }