

// FUTURO CARROSSEL
const carrossel = document.querySelector('.carrossel');
const btnanterior = document.querySelector('.anterior');
const btnproximo = document.querySelector('.proximo');
const itens = document.querySelectorAll('.itens');

function scrollCarousel(direction) {
    if (carrossel) {
        
        const scrollAmount = carrossel.clientWidth;
        
        
        carrossel.scrollBy({ 
            left: scrollAmount * direction, 
            behavior: 'smooth' 
        });
    }
}


if (carrossel && btnanterior && btnproximo && itens.length > 0) {
    
  
    btnproximo.addEventListener('click', () => {
        scrollCarousel(1); // Rola para a direita
    });

   
    btnanterior.addEventListener('click', () => {
        scrollCarousel(-1); 
    });
}


// MENU DROPDOWN

document.addEventListener('DOMContentLoaded', function() {
    // Seleciona todos os itens de menu que têm um dropdown
    const dropdowns = document.querySelectorAll('.has-dropdown');

    dropdowns.forEach(dropdown => {
        const trigger = dropdown.querySelector('a'); 

        trigger.addEventListener('click', function(event) {
            
            event.preventDefault();

        
            document.querySelectorAll('.has-dropdown.is-open').forEach(openDropdown => {
                if (openDropdown !== dropdown) {
                    openDropdown.classList.remove('is-open');
                }
            });

            // Adiciona ou remove a classe 'is-open' no item de menu clicado
            dropdown.classList.toggle('is-open');
        });
    });

    // Fecha o dropdown se o usuário clicar fora dele
    window.addEventListener('click', function(event) {
        // Verifica se o clique não foi dentro de um item com dropdown
        if (!event.target.closest('.has-dropdown')) {
            // Se não foi, remove a classe 'is-open' de todos os dropdowns
            document.querySelectorAll('.has-dropdown.is-open').forEach(openDropdown => {
                openDropdown.classList.remove('is-open');
            });
        }
    });
});



// --- INÍCIO: LÓGICA DA ANIMAÇÃO REVEAL AO ROLAR ---

document.addEventListener('DOMContentLoaded', () => {
    // 1. Seleciona todos os elementos que devem ser animados
    const elementsToReveal = document.querySelectorAll('.reveal-on-scroll');

    // 2. Cria o "observador"
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            // 3. Se o elemento está visível na tela...
            if (entry.isIntersecting) {
                // 4. ...adiciona a classe '.is-visible' para disparar a animação
                entry.target.classList.add('is-visible');
                // 5. (Opcional) Para a observação para que a animação aconteça só uma vez
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1 // A animação dispara quando 10% do elemento está visível
    });

    // 6. Inicia a observação para cada elemento
    elementsToReveal.forEach(element => {
        observer.observe(element);
    });
});

// --- FIM: LÓGICA DA ANIMAÇÃO REVEAL AO ROLAR ---
/* JS/index.js */

// --- INÍCIO: LÓGICA DO BOTÃO VOLTAR AO TOPO ---

document.addEventListener('DOMContentLoaded', () => {
    // 1. Seleciona o botão
    const backToTopButton = document.getElementById('back-to-top-btn');

    // 2. Adiciona um "ouvinte" para o evento de rolagem da página
    window.addEventListener('scroll', () => {
        // 3. Se o usuário rolou mais de 300 pixels para baixo...
        if (window.scrollY > 300) {
            // ...adiciona a classe que torna o botão visível
            backToTopButton.classList.add('is-visible');
        } else {
            // ...caso contrário, remove a classe
            backToTopButton.classList.remove('is-visible');
        }
    });

    // 4. Adiciona um "ouvinte" para o evento de clique no botão
    backToTopButton.addEventListener('click', () => {
        // 5. Rola a página suavemente de volta para o topo
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
});
