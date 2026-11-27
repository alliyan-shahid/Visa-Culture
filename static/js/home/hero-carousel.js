
    const heroCarousel = document.getElementById('heroCarousel');
    const heroSlides = document.querySelectorAll('.hero-slide');
    const heroDots = document.querySelectorAll('.hero-dot');
    const heroPrevBtn = document.getElementById('heroPrevBtn');
    const heroNextBtn = document.getElementById('heroNextBtn');

    let currentSlide = 0;
    let autoplayInterval = null;
    const SLIDE_DURATION = 5000; // 5 seconds
    const TRANSITION_DURATION = 1200; // 1.2 seconds

    function showSlide(index) {
        // Update slides
        heroSlides.forEach((slide, i) => {
            slide.classList.remove('active');
            if (i === index) {
                slide.classList.add('active');
            }
        });

        // Update dots
        heroDots.forEach((dot, i) => {
            dot.classList.remove('active');
            if (i === index) {
                dot.classList.add('active');
            }
        });

        currentSlide = index;
    }

    function nextSlide() {
        let next = (currentSlide + 1) % heroSlides.length;
        showSlide(next);
        resetAutoplay();
    }

    function prevSlide() {
        let prev = (currentSlide - 1 + heroSlides.length) % heroSlides.length;
        showSlide(prev);
        resetAutoplay();
    }

    function goToSlide(index) {
        showSlide(index);
        resetAutoplay();
    }

    function startAutoplay() {
        if (autoplayInterval) {
            clearInterval(autoplayInterval);
        }
        autoplayInterval = setInterval(() => {
            nextSlide();
        }, SLIDE_DURATION);
    }

    function resetAutoplay() {
        if (autoplayInterval) {
            clearInterval(autoplayInterval);
        }
        startAutoplay();
    }

    // Event listeners
    heroPrevBtn.addEventListener('click', prevSlide);
    heroNextBtn.addEventListener('click', nextSlide);

    heroDots.forEach(dot => {
        dot.addEventListener('click', (e) => {
            goToSlide(parseInt(e.target.dataset.slide));
        });
    });

    // Pause autoplay on hover
    heroCarousel.addEventListener('mouseenter', () => {
        if (autoplayInterval) {
            clearInterval(autoplayInterval);
            autoplayInterval = null;
        }
    });

    heroCarousel.addEventListener('mouseleave', () => {
        startAutoplay();
    });

    // Start autoplay on load
    startAutoplay();

    // Touch support for mobile
    let touchStartX = 0;
    let touchEndX = 0;

    heroCarousel.addEventListener('touchstart', (e) => {
        touchStartX = e.changedTouches[0].screenX;
    });

    heroCarousel.addEventListener('touchend', (e) => {
        touchEndX = e.changedTouches[0].screenX;
        if (touchStartX - touchEndX > 50) {
            nextSlide();
        } else if (touchEndX - touchStartX > 50) {
            prevSlide();
        }
    });
