/* JS/main.js - Verifique seu arquivo contra este código */

function pageTransitions() {
    document.documentElement.classList.add('js-enabled');

    // FADE-IN AO CARREGAR
    window.addEventListener('DOMContentLoaded', () => {
        document.body.classList.add('fade-in');
    });

    // FADE-OUT AO CLICAR EM LINKS
    const allLinks = document.querySelectorAll('a');

    allLinks.forEach(link => {
        link.addEventListener('click', event => {
            const href = link.getAttribute('href');

            if (!href || href.startsWith('#') || link.target === '_blank' || href.startsWith('mailto:') || href.startsWith('tel:')) {
                return;
            }

            event.preventDefault(); // Previne a navegação imediata

            document.body.classList.add('fade-out');

            // Navega após a animação
            setTimeout(() => {
                window.location.href = href;
            }, 500); 
        });
    });
}

pageTransitions();