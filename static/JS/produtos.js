// ==========================================
// PRODUTOS.JS - Smart Paws
// ==========================================

// ========== FUNÇÃO PARA OBTER CSRF TOKEN ==========
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

document.addEventListener('DOMContentLoaded', function() {
    
    // ========== AUTO-SUBMIT DOS FILTROS ==========
    const formFiltros = document.getElementById('form-filtros');
    const checkboxPromo = document.querySelector('input[name="em_promocao"]');
    const selectCategoria = document.getElementById('filtro-categoria');
    
    if (checkboxPromo) {
        checkboxPromo.addEventListener('change', function() {
            formFiltros.submit();
        });
    }
    
    if (selectCategoria) {
        selectCategoria.addEventListener('change', function() {
            formFiltros.submit();
        });
    }
    
    // ========== TOGGLE VIEW (GRID/LIST) ==========
    const btnViews = document.querySelectorAll('.btn-view');
    const produtosContainer = document.getElementById('produtos-container');
    
    btnViews.forEach(btn => {
        btn.addEventListener('click', function() {
            const view = this.getAttribute('data-view');
            
            // Remove active de todos
            btnViews.forEach(b => b.classList.remove('active'));
            
            // Adiciona active no clicado
            this.classList.add('active');
            
            // Muda o layout
            if (view === 'list') {
                produtosContainer.classList.add('produtos-list');
                produtosContainer.classList.remove('produtos-grid');
            } else {
                produtosContainer.classList.add('produtos-grid');
                produtosContainer.classList.remove('produtos-list');
            }
            
            // Salva preferência no localStorage
            localStorage.setItem('viewMode', view);
        });
    });
    
    // Carrega preferência salva
    const savedView = localStorage.getItem('viewMode');
    if (savedView === 'list') {
        document.querySelector('.btn-view[data-view="list"]')?.click();
    }
    
    // ========== BUSCA COM DEBOUNCE ==========
    const buscaInput = document.getElementById('busca-produtos');
    let timeoutBusca;
    
    if (buscaInput) {
        buscaInput.addEventListener('input', function() {
            clearTimeout(timeoutBusca);
            
            timeoutBusca = setTimeout(() => {
                if (this.value.length >= 3 || this.value.length === 0) {
                    formFiltros.submit();
                }
            }, 800);
        });
    }
    
    // ========== ADICIONAR AO CARRINHO VIA AJAX ==========
    const formsCarrinho = document.querySelectorAll('.form-adicionar-carrinho');
    
    formsCarrinho.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const url = this.action;
            const csrftoken = getCookie('csrftoken');
            const button = this.querySelector('button[type="submit"]');
            const originalText = button.innerHTML;
            
            // Feedback visual
            button.disabled = true;
            button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Adicionando...';
            
            // Requisição AJAX com Fetch API
            fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrftoken
                },
                credentials: 'same-origin'
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro na requisição');
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    // Feedback de sucesso
                    button.innerHTML = '<i class="fas fa-check"></i> Adicionado!';
                    button.style.backgroundColor = '#28a745';
                    
                    // Atualizar contador do carrinho
                    atualizarContadorCarrinho(data.total_itens);
                    
                    // Mostrar notificação
                    mostrarNotificacao(data.message, 'success');
                    
                    // Restaurar botão após 2 segundos
                    setTimeout(() => {
                        button.disabled = false;
                        button.innerHTML = originalText;
                        button.style.backgroundColor = '';
                    }, 2000);
                } else {
                    throw new Error(data.error || 'Erro ao adicionar produto');
                }
            })
            .catch(error => {
                console.error('Erro:', error);
                button.disabled = false;
                button.innerHTML = originalText;
                mostrarNotificacao('Erro ao adicionar produto ao carrinho', 'error');
            });
        });
    });
    
    // ========== ATUALIZAR CONTADOR CARRINHO ==========
    function atualizarContadorCarrinho(totalItens) {
        const contadores = document.querySelectorAll('.carrinho-count, .carrinho-contador');
        
        contadores.forEach(contador => {
            if (contador) {
                contador.textContent = totalItens;
                
                // Animação pulse
                contador.classList.add('pulse');
                setTimeout(() => contador.classList.remove('pulse'), 500);
            }
        });
    }
    
    // ========== FUNÇÃO PARA MOSTRAR NOTIFICAÇÕES ==========
    function mostrarNotificacao(mensagem, tipo) {
        // Remove notificação anterior se existir
        const notificacaoAnterior = document.querySelector('.notificacao-carrinho');
        if (notificacaoAnterior) {
            notificacaoAnterior.remove();
        }
        
        // Criar nova notificação
        const notificacao = document.createElement('div');
        notificacao.className = `notificacao-carrinho ${tipo}`;
        notificacao.innerHTML = `
            <i class="fas ${tipo === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'}"></i>
            <span>${mensagem}</span>
        `;
        
        document.body.appendChild(notificacao);
        
        // Mostrar notificação com animação
        setTimeout(() => notificacao.classList.add('show'), 100);
        
        // Remover após 3 segundos
        setTimeout(() => {
            notificacao.classList.remove('show');
            setTimeout(() => notificacao.remove(), 300);
        }, 3000);
    }
    
    // ========== SMOOTH SCROLL ==========
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // ========== LOADING STATE ==========
    const formOrdenacao = document.querySelector('.form-ordenacao select');
    if (formOrdenacao) {
        formOrdenacao.addEventListener('change', function() {
            // Mostrar loading
            if (produtosContainer) {
                produtosContainer.style.opacity = '0.5';
                produtosContainer.style.pointerEvents = 'none';
            }
        });
    }
    
    // ========== LAZY LOADING IMAGES ==========
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                    }
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        document.querySelectorAll('img[loading="lazy"]').forEach(img => {
            imageObserver.observe(img);
        });
    }
    
    // ========== ANIMAÇÃO DE ENTRADA DOS CARDS ==========
    if ('IntersectionObserver' in window) {
        const cardObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.animation = 'fadeInUp 0.6s ease forwards';
                    cardObserver.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1
        });
        
        // Observa todos os cards
        document.querySelectorAll('.card-produto').forEach(card => {
            cardObserver.observe(card);
        });
    }
});

// ========== ESTILOS CSS DINÂMICOS ==========
const style = document.createElement('style');
style.textContent = `
    /* Animação Fade In Up */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .card-produto {
        opacity: 0;
    }
    
    /* Animação Pulse */
    .pulse {
        animation: pulse 0.5s ease;
    }
    
    @keyframes pulse {
        0%, 100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.3);
        }
    }
    
    /* Notificação do Carrinho */
    .notificacao-carrinho {
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 25px;
        background: white;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        display: flex;
        align-items: center;
        gap: 12px;
        z-index: 10000;
        transform: translateX(400px);
        transition: transform 0.3s ease;
        max-width: 350px;
    }
    
    .notificacao-carrinho.show {
        transform: translateX(0);
    }
    
    .notificacao-carrinho.success {
        border-left: 4px solid #ab8262;;
    }
    
    .notificacao-carrinho.error {
        border-left: 4px solid #ab8262;
    }
    
    .notificacao-carrinho i {
        font-size: 20px;
        flex-shrink: 0;
    }
    
    .notificacao-carrinho.success i {
        color: #28a745;
    }
    
    .notificacao-carrinho.error i {
        color: #dc3545;
    }
    
    .notificacao-carrinho span {
        font-weight: 500;
        color: #333;
        font-size: 14px;
    }
    
    /* Spinner animation */
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .fa-spinner.fa-spin {
        animation: spin 1s linear infinite;
    }
`;
document.head.appendChild(style);
