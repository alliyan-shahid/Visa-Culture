
        (function() {
            const bookWidget = document.getElementById('bookWidget');
            const bookBtn = document.getElementById('bookBtn');
            const bookMenu = document.getElementById('bookMenu');
            if (!bookWidget || !bookBtn || !bookMenu) return;

            function closeBookMenu() { bookMenu.classList.remove('is-open'); bookBtn.setAttribute('aria-expanded', 'false'); }
            function openBookMenu() { bookMenu.classList.add('is-open'); bookBtn.setAttribute('aria-expanded', 'true'); }

            bookBtn.addEventListener('click', function(e) {
                e.stopPropagation();
                if (bookMenu.classList.contains('is-open')) closeBookMenu();
                else openBookMenu();
            });

            document.addEventListener('click', function(e) { if (!bookWidget.contains(e.target)) closeBookMenu(); });
            document.addEventListener('keydown', function(e) { if (e.key === 'Escape') closeBookMenu(); });
        })();

        (function () {
            const widget = document.getElementById('whatsappWidget');
            const btn = document.getElementById('whatsappBtn');
            const menu = document.getElementById('whatsappMenu');
            if (!widget || !btn || !menu) return;

            function closeMenu() { menu.classList.remove('is-open'); btn.setAttribute('aria-expanded', 'false'); }
            function openMenu() { menu.classList.add('is-open'); btn.setAttribute('aria-expanded', 'true'); }

            btn.addEventListener('click', function (e) {
                e.stopPropagation();
                if (menu.classList.contains('is-open')) closeMenu();
                else openMenu();
            });

            document.addEventListener('click', function (e) { if (!widget.contains(e.target)) closeMenu(); });
            document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeMenu(); });
        })();
    