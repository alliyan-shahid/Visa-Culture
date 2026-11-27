
    function toggleAustraliaCards(event) {
        event.preventDefault();
        const btn = event.currentTarget;
        const section = document.getElementById('ideaCarouselSection');
        const expanded = section.classList.toggle('is-expanded');

        btn.setAttribute('aria-expanded', expanded ? 'true' : 'false');
        btn.textContent = expanded ? 'Show Less' : 'Show More';
    }

    function initMobileTextCollapse() {
        if (window.innerWidth > 768) return;

        const candidates = document.querySelectorAll('section p');
        candidates.forEach((paragraph) => {
            if (paragraph.dataset.mobileProcessed === 'true') return;
            if (paragraph.closest('.hero-content')) return;
            if (paragraph.closest('form')) return;
            if (paragraph.closest('#budget-guidance')) return;
            if (paragraph.closest('#services')) return;
            if (paragraph.closest('#ielts-pte')) return;

            const text = paragraph.textContent ? paragraph.textContent.trim() : '';
            if (text.length < 170) return;

            paragraph.style.setProperty('--mobile-line-clamp', '5');
            paragraph.classList.add('mobile-text-collapsed');
            paragraph.dataset.mobileProcessed = 'true';

            const toggleBtn = document.createElement('button');
            toggleBtn.type = 'button';
            toggleBtn.className = 'mobile-text-toggle';
            toggleBtn.textContent = 'View More';

            toggleBtn.addEventListener('click', () => {
                const expanded = paragraph.classList.toggle('mobile-text-collapsed');
                toggleBtn.textContent = expanded ? 'View More' : 'View Less';
            });

            paragraph.insertAdjacentElement('afterend', toggleBtn);
        });

    }

    document.addEventListener('DOMContentLoaded', initMobileTextCollapse);
