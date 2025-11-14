// ==========================================
// INDEX.JS - Smart Paws (CORRIGIDO)
// ==========================================

// ==========================================
// CARROSSEL
// ==========================================
document.addEventListener('DOMContentLoaded', () => {
    const track = document.querySelector('.carrossel-track');
    const btnAnterior = document.querySelector('.carrossel-nav.anterior');
    const btnProximo = document.querySelector('.carrossel-nav.proximo');
    const items = document.querySelectorAll('.carrossel-item');
    
    // ✅ CORREÇÃO: Verifica se os elementos existem antes de continuar
    if (!track || !items.length || !btnAnterior || !btnProximo) {
        console.log('Carrossel não encontrado nesta página');
        return;
    }
    
    let currentIndex = 0;
    let itemsPerView = 3;
    let autoplayInterval;
    const autoplayDelay = 5000;
    
    function updateItemsPerView() {
        const width = window.innerWidth;
        if (width <= 768) {
            itemsPerView = 1;
        } else if (width <= 1024) {
            itemsPerView = 2;
        } else {
            itemsPerView = 3;
        }
    }
    
    function updateCarousel() {
        const itemWidth = items[0].offsetWidth;
        const gap = 20;
        const offset = -(currentIndex * (itemWidth + gap));
        track.style.transform = `translateX(${offset}px)`;
        
        btnAnterior.disabled = currentIndex === 0;
        btnProximo.disabled = currentIndex >= items.length - itemsPerView;
    }
    
    function nextSlide() {
        if (currentIndex < items.length - itemsPerView) {
            currentIndex++;
            updateCarousel();
        } else {
            currentIndex = 0;
            updateCarousel();
        }
    }
    
    function prevSlide() {
        if (currentIndex > 0) {
            currentIndex--;
            updateCarousel();
        }
    }
    
    function startAutoplay() {
        autoplayInterval = setInterval(nextSlide, autoplayDelay);
    }
    
    function stopAutoplay() {
        clearInterval(autoplayInterval);
    }
    
    // Event listeners
    btnProximo.addEventListener('click', () => {
        nextSlide();
        stopAutoplay();
        startAutoplay();
    });
    
    btnAnterior.addEventListener('click', () => {
        prevSlide();
        stopAutoplay();
        startAutoplay();
    });
    
    track.addEventListener('mouseenter', stopAutoplay);
    track.addEventListener('mouseleave', startAutoplay);
    
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowLeft') {
            prevSlide();
            stopAutoplay();
            startAutoplay();
        } else if (e.key === 'ArrowRight') {
            nextSlide();
            stopAutoplay();
            startAutoplay();
        }
    });
    
    let touchStartX = 0;
    let touchEndX = 0;
    
    track.addEventListener('touchstart', (e) => {
        touchStartX = e.changedTouches[0].screenX;
        stopAutoplay();
    });
    
    track.addEventListener('touchend', (e) => {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
        startAutoplay();
    });
    
    function handleSwipe() {
        const swipeThreshold = 50;
        const diff = touchStartX - touchEndX;
        
        if (Math.abs(diff) > swipeThreshold) {
            if (diff > 0) {
                nextSlide();
            } else {
                prevSlide();
            }
        }
    }
    
    window.addEventListener('resize', () => {
        updateItemsPerView();
        currentIndex = 0;
        updateCarousel();
    });
    
    updateItemsPerView();
    updateCarousel();
    startAutoplay();
});

// ==========================================
// MENU DROPDOWN
// ==========================================
document.addEventListener('DOMContentLoaded', function() {
    const dropdowns = document.querySelectorAll('.has-dropdown');
    
    // ✅ CORREÇÃO: Verifica se há dropdowns na página
    if (!dropdowns.length) {
        console.log('Nenhum dropdown encontrado nesta página');
        return;
    }

    dropdowns.forEach(dropdown => {
        const trigger = dropdown.querySelector('a');
        
        // ✅ CORREÇÃO: Verifica se o trigger existe
        if (!trigger) return;

        trigger.addEventListener('click', function(event) {
            if (trigger.getAttribute('href') === '#') {
                event.preventDefault();

                document.querySelectorAll('.has-dropdown.is-open').forEach(openDropdown => {
                    if (openDropdown !== dropdown) {
                        openDropdown.classList.remove('is-open');
                    }
                });

                dropdown.classList.toggle('is-open');
            }
        });
    });

    window.addEventListener('click', function(event) {
        if (!event.target.closest('.has-dropdown')) {
            document.querySelectorAll('.has-dropdown.is-open').forEach(openDropdown => {
                openDropdown.classList.remove('is-open');
            });
        }
    });
});

// ==========================================
// ANIMAÇÃO REVEAL AO ROLAR
// ==========================================
document.addEventListener('DOMContentLoaded', () => {
    const elementsToReveal = document.querySelectorAll('.reveal-on-scroll');
    
    // ✅ CORREÇÃO: Verifica se há elementos para animar
    if (!elementsToReveal.length) {
        console.log('Nenhum elemento para revelar nesta página');
        return;
    }

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1
    });

    elementsToReveal.forEach(element => {
        observer.observe(element);
    });
});

// ==========================================
// BOTÃO VOLTAR AO TOPO
// ==========================================
document.addEventListener('DOMContentLoaded', () => {
    const backToTopButton = document.getElementById('back-to-top-btn');
    
    // ✅ CORREÇÃO: Verifica se o botão existe
    if (!backToTopButton) {
        console.log('Botão voltar ao topo não encontrado nesta página');
        return;
    }

    window.addEventListener('scroll', () => {
        if (window.scrollY > 300) {
            backToTopButton.classList.add('is-visible');
        } else {
            backToTopButton.classList.remove('is-visible');
        }
    });

    backToTopButton.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
});
