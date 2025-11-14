document.addEventListener('DOMContentLoaded', () => {
    initCarrinho();
    updateCarrinhoCount();
});

function initCarrinho() {
    // Botões de quantidade
    const btnQtd = document.querySelectorAll('.btn-qtd');
    btnQtd.forEach(btn => {
        btn.addEventListener('click', handleQuantityClick);
    });
    
    // Inputs de quantidade
    const qtdInputs = document.querySelectorAll('.qtd-input');
    qtdInputs.forEach(input => {
        input.addEventListener('change', handleQuantityChange);
    });
    
    // Botões de remover
    const btnRemover = document.querySelectorAll('.btn-remover');
    btnRemover.forEach(btn => {
        btn.addEventListener('click', handleRemoveItem);
    });
}

// Altera quantidade com botões +/-
async function handleQuantityClick(e) {
    const button = e.currentTarget;
    const itemId = button.dataset.itemId;
    const action = button.dataset.action;
    const input = document.querySelector(`.qtd-input[data-item-id="${itemId}"]`);
    
    let currentQtd = parseInt(input.value);
    
    if (action === 'increase') {
        currentQtd++;
    } else if (action === 'decrease' && currentQtd > 1) {
        currentQtd--;
    }
    
    input.value = currentQtd;
    await updateQuantity(itemId, currentQtd);
}

// Altera quantidade digitando
async function handleQuantityChange(e) {
    const input = e.currentTarget;
    const itemId = input.dataset.itemId;
    const quantidade = parseInt(input.value);
    
    if (quantidade > 0) {
        await updateQuantity(itemId, quantidade);
    } else {
        input.value = 1;
    }
}

// Atualiza quantidade via AJAX
async function updateQuantity(itemId, quantidade) {
    try {
        const formData = new FormData();
        formData.append('quantidade', quantidade);
        formData.append('csrfmiddlewaretoken', getCsrfToken());
        
        const response = await fetch(`/carrinho/atualizar/${itemId}/`, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            },
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Atualiza total do item
            document.getElementById(`item-total-${itemId}`).textContent = 
                `R$ ${formatMoney(data.item_total)}`;
            
            // Atualiza resumo
            document.getElementById('carrinho-subtotal').textContent = 
                `R$ ${formatMoney(data.carrinho_subtotal)}`;
            
            document.getElementById('carrinho-total').textContent = 
                `R$ ${formatMoney(data.carrinho_total)}`;
            
            showNotification('Carrinho atualizado!', 'success');
        }
    } catch (error) {
        console.error('Erro ao atualizar quantidade:', error);
        showNotification('Erro ao atualizar carrinho', 'error');
    }
}

// Remove item do carrinho
async function handleRemoveItem(e) {
    const button = e.currentTarget;
    const itemId = button.dataset.itemId;
    
    if (!confirm('Deseja remover este item do carrinho?')) return;
    
    try {
        const formData = new FormData();
        formData.append('csrfmiddlewaretoken', getCsrfToken());
        
        const response = await fetch(`/carrinho/remover/${itemId}/`, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            },
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Remove o card do item
            const itemCard = document.querySelector(`.item-card[data-item-id="${itemId}"]`);
            itemCard.style.opacity = '0';
            itemCard.style.transform = 'translateX(-20px)';
            
            setTimeout(() => {
                itemCard.remove();
                
                // Verifica se ainda há itens
                const remainingItems = document.querySelectorAll('.item-card');
                if (remainingItems.length === 0) {
                    location.reload(); // Recarrega para mostrar "carrinho vazio"
                } else {
                    // Atualiza resumo
                    document.getElementById('carrinho-subtotal').textContent = 
                        `R$ ${formatMoney(data.carrinho_subtotal)}`;
                    
                    document.getElementById('carrinho-total').textContent = 
                        `R$ ${formatMoney(data.carrinho_total)}`;
                    
                    updateCarrinhoCount();
                }
            }, 300);
            
            showNotification('Item removido do carrinho', 'success');
        }
    } catch (error) {
        console.error('Erro ao remover item:', error);
        showNotification('Erro ao remover item', 'error');
    }
}

// Atualiza contador do carrinho no header
async function updateCarrinhoCount() {
    try {
        const response = await fetch('/carrinho/api/count/', {
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            }
        });
        
        const data = await response.json();
        
        const badge = document.getElementById('carrinho-count');
        if (badge) {
            badge.textContent = data.count;
            
            if (data.count > 0) {
                badge.style.display = 'flex';
            } else {
                badge.style.display = 'none';
            }
        }
    } catch (error) {
        console.error('Erro ao atualizar contador:', error);
    }
}

// Adiciona produto ao carrinho (para usar em produtos.html)
async function adicionarAoCarrinho(produtoId, quantidade = 1) {
    try {
        const formData = new FormData();
        formData.append('quantidade', quantidade);
        formData.append('csrfmiddlewaretoken', getCsrfToken());
        
        const response = await fetch(`/carrinho/adicionar/${produtoId}/`, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            },
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification(data.message, 'success');
            updateCarrinhoCount();
            
            // Animação do botão
            const btn = event.target.closest('button');
            if (btn) {
                const originalText = btn.innerHTML;
                btn.innerHTML = '<i class="fas fa-check"></i> Adicionado!';
                btn.style.backgroundColor = '#28a745';
                
                setTimeout(() => {
                    btn.innerHTML = originalText;
                    btn.style.backgroundColor = '';
                }, 2000);
            }
        }
    } catch (error) {
        console.error('Erro ao adicionar ao carrinho:', error);
        showNotification('Erro ao adicionar produto', 'error');
    }
}

// Funções utilitárias
function getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
}

function formatMoney(value) {
    return parseFloat(value).toFixed(2).replace('.', ',');
}

function showNotification(message, type = 'info') {
    // Cria elemento de notificação
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
        <span>${message}</span>
    `;
    
    document.body.appendChild(notification);
    
    // Mostra com animação
    setTimeout(() => notification.classList.add('show'), 10);
    
    // Remove após 3 segundos
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Adiciona CSS das notificações dinamicamente
const notificationStyles = document.createElement('style');
notificationStyles.textContent = `
    .notification {
        position: fixed;
        top: 20px;
        right: 20px;
        background: white;
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        display: flex;
        align-items: center;
        gap: 10px;
        z-index: 10000;
        transform: translateX(400px);
        transition: transform 0.3s ease;
        font-family: "Montserrat", sans-serif;
        font-size: 14px;
    }
    
    .notification.show {
        transform: translateX(0);
    }
    
    .notification-success {
        border-left: 4px solid #28a745;
        color: #28a745;
    }
    
    .notification-error {
        border-left: 4px solid #dc3545;
        color: #dc3545;
    }
    
    .notification i {
        font-size: 20px;
    }
`;
document.head.appendChild(notificationStyles);