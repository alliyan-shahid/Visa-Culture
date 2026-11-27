
    (function () {
        const stage = document.querySelector('[data-services-stage]');
        if (!stage) return;
        const tabs = Array.from(stage.querySelectorAll('[data-service-tab]'));
        const slides = Array.from(stage.querySelectorAll('[data-service-slide]'));
        const counter = stage.querySelector('[data-service-count]');
        const progress = stage.querySelector('[data-service-progress]');
        const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        let active = 0;
        let timer;

        function showService(index) {
            active = (index + slides.length) % slides.length;
            tabs.forEach((tab, i) => {
                const selected = i === active;
                tab.classList.toggle('is-active', selected);
                tab.setAttribute('aria-selected', selected ? 'true' : 'false');
            });
            slides.forEach((slide, i) => {
                slide.classList.toggle('is-active', i === active);
                slide.classList.toggle('is-next', i === (active + 1) % slides.length);
                slide.classList.toggle('is-prev', i === (active - 1 + slides.length) % slides.length);
                slide.classList.toggle('is-next-two', i === (active + 2) % slides.length);
            });
            if (counter) counter.textContent = String(active + 1).padStart(2, '0');
            if (progress) progress.style.width = `${((active + 1) / slides.length) * 100}%`;
        }

        function start() {
            if (!reduceMotion) timer = window.setInterval(() => showService(active + 1), 4000);
        }
        function reset() { window.clearInterval(timer); start(); }

        tabs.forEach((tab, index) => tab.addEventListener('click', () => { showService(index); reset(); }));
        showService(0);
        start();
    }());
