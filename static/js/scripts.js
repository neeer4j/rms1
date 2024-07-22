document.addEventListener("DOMContentLoaded", () => {
    handleFlashes();
    initLazyLoadImages();
    initModals();
    initAnimations();
    showModal();
});

function handleFlashes() {
    const flashes = document.querySelectorAll('.flashes li');
    flashes.forEach(flash => {
        setTimeout(() => {
            flash.style.transition = "opacity 1s, height 1s, margin 1s, padding 1s";
            flash.style.opacity = "0";
            flash.style.height = "0";
            flash.style.margin = "0";
            flash.style.padding = "0";
            setTimeout(() => {
                flash.remove();
            }, 1000);
        }, 3000);
    });
}

function initLazyLoadImages() {
    const lazyImages = document.querySelectorAll('img.lazy');

    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const image = entry.target;
                image.src = image.dataset.src;
                image.classList.remove('lazy');
                observer.unobserve(image);
            }
        });
    });

    lazyImages.forEach(image => {
        imageObserver.observe(image);
    });
}

function initModals() {
    const openModalButtons = document.querySelectorAll('[data-modal-target]');
    const closeModalButtons = document.querySelectorAll('[data-close-button]');
    const overlay = document.getElementById('overlay');

    openModalButtons.forEach(button => {
        button.addEventListener('click', () => {
            const modal = document.querySelector(button.dataset.modalTarget);
            openModal(modal);
        });
    });

    closeModalButtons.forEach(button => {
        button.addEventListener('click', () => {
            const modal = button.closest('.modal');
            closeModal(modal);
        });
    });

    overlay.addEventListener('click', () => {
        const modals = document.querySelectorAll('.modal.active');
        modals.forEach(modal => {
            closeModal(modal);
        });
    });

    function openModal(modal) {
        if (modal == null) return;
        modal.classList.add('active');
        overlay.classList.add('active');
    }

    function closeModal(modal) {
        if (modal == null) return;
        modal.classList.remove('active');
        overlay.classList.remove('active');
    }
}

function initAnimations() {
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    
    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    animatedElements.forEach(element => {
        observer.observe(element);
    });
}

function showModal() {
    const successModal = document.getElementById('success-modal');
    const closeModal = document.getElementById('close-modal');
    
    if (successModal) {
        successModal.classList.add('active');
    }

    if (closeModal) {
        closeModal.addEventListener('click', () => {
            successModal.classList.remove('active');
        });
    }
}
