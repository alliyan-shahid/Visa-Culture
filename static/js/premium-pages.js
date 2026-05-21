// Premium page interactions: smooth card hovers and simple page transitions
(function(){
    // Add subtle hover lift to all university cards on the homepage
    try {
        document.querySelectorAll('#universities a').forEach(card => {
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
                    document.documentElement.style.transition = 'opacity 320ms ease';
                    document.documentElement.style.opacity = '0';
                    setTimeout(() => { window.location = href; }, 280);
                });
            }
        });

        // fade in on load
        document.addEventListener('DOMContentLoaded', function(){
            document.documentElement.style.opacity = '0';
            setTimeout(()=>{ document.documentElement.style.transition = 'opacity 420ms ease'; document.documentElement.style.opacity = '1'; }, 40);
        });
    } catch (e) {
        console.warn('premium transition init error', e);
    }
})();
