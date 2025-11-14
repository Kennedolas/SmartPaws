// ==========================================
// static/JS/utils.js - UTILITIES
// ==========================================

/**
 * Funções auxiliares usadas em várias páginas
 */

// ========== ADICIONAR AO CARRINHO ==========
function adicionarAoCarrinho(produtoId, quantidade = 1) {
    const csrftoken = getCookie('csrftoken');
    
    fetch('/carrinho/adicionar/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            produto_id: produtoId,
            quantidade: quantidade
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            mostrarNotificacao('Produto adicionado ao carrinho!', 'success');
            atualizarContadorCarrinho(data.total_itens);
        } else {
            mostrarNotificacao('Erro ao adicionar produto', 'error');
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        mostrarNotificacao('Erro ao adicionar produto', 'error');
    });
}

// ========== GET CSRF TOKEN ==========
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// ========== NOTIFICAÇÕES ==========
function mostrarNotificacao(mensagem, tipo = 'info') {
    const notificacao = document.createElement('div');
    notificacao.className = `notificacao notificacao-${tipo}`;
    notificacao.textContent = mensagem;
    
    document.body.appendChild(notificacao);
    
    setTimeout(() => {
        notificacao.classList.add('mostrar');
    }, 100);
    
    setTimeout(() => {
        notificacao.classList.remove('mostrar');
        setTimeout(() => {
            notificacao.remove();
        }, 300);
    }, 3000);
}

// ========== ATUALIZAR CONTADOR CARRINHO ==========
function atualizarContadorCarrinho(total) {
    const contador = document.querySelector('.carrinho-contador');
    if (contador) {
        contador.textContent = total;
        contador.classList.add('pulse');
        setTimeout(() => contador.classList.remove('pulse'), 500);
    }
}

// ========== FORMATAR PREÇO ==========
function formatarPreco(valor) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(valor);
}

// ========== VALIDAR EMAIL ==========
function validarEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// ========== DEBOUNCE ==========
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}
