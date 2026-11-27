        function replaceFeatherIcons() {
            if (window.feather) {
                try {
                    feather.replace({ 'stroke-width': 2, width: '24', height: '24' });
                } catch (e) {
                    console.warn('feather replace failed', e);
                }
            } else {
                console.warn('feather icons library is not available');
            }
        }

        if (document.readyState === 'complete') {
            replaceFeatherIcons();
        } else {
            window.addEventListener('load', replaceFeatherIcons);
        }

        document.getElementById('navToggle')?.addEventListener('click', function() {
            document.getElementById('mobileMenu')?.classList.toggle('hidden');
        });

