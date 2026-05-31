// Premium page interactions: smooth card hovers and simple page transitions
(function(){
    const root = document.documentElement;

    function showPage(animate = true) {
        root.style.transition = animate ? 'opacity 420ms ease' : 'none';
        root.style.opacity = '1';
    }

    // Add subtle hover lift to university cards on the network page
    try {
        document.querySelectorAll('[data-university-card]').forEach(card => {
            card.addEventListener('mouseenter', () => card.classList.add('hovered'));
            card.addEventListener('mouseleave', () => card.classList.remove('hovered'));
        });
    } catch (e) {
        console.warn('premium hover init error', e);
    }

    // Simple fade transition when navigating between pages
    try {
        const links = Array.from(document.querySelectorAll('a'));
        links.forEach(a => {
            // only attach to internal links
            const href = a.getAttribute('href') || '';
            if (href.startsWith('/') || href.startsWith(location.origin)) {
                a.addEventListener('click', function(e){
                    // allow modifier-clicks and anchors
                    if (e.metaKey || e.ctrlKey || e.shiftKey || a.target === '_blank' || href.startsWith('#')) return;
                    e.preventDefault();
                    root.style.transition = 'opacity 320ms ease';
                    root.style.opacity = '0';
                    setTimeout(() => { window.location = href; }, 280);
                });
            }
        });

        // fade in on load
        document.addEventListener('DOMContentLoaded', function(){
            root.style.opacity = '0';
            setTimeout(showPage, 40);
        });

        // Browsers can restore the page from the back/forward cache with the
        // previous inline opacity still set to 0, so make restores visible too.
        window.addEventListener('pageshow', function(event) {
            if (event.persisted) showPage(false);
        });

        // Reset before bfcache snapshots the page, otherwise Back can restore
        // the hidden transition state and leave the page looking blank.
        window.addEventListener('pagehide', function() {
            showPage(false);
        });
    } catch (e) {
        console.warn('premium transition init error', e);
    }
})();
