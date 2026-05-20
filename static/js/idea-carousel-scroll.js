/**
 * Simple carousel controller.
 * No 3D effects, no section takeover, no complex gesture logic.
 */
(function () {
    'use strict';

    function init() {
        var carousel = document.getElementById('ideaCarousel');
        if (!carousel) return;

        var cards = Array.from(carousel.querySelectorAll('.carousel-card'));
        if (!cards.length) return;

        // Clear any inline styles left by previous advanced animations.
        cards.forEach(function (card) {
            card.style.transform = '';
            card.style.opacity = '';
            card.style.filter = '';
            card.style.zIndex = '';
            card.style.transition = '';
            card.style.border = '';
            card.style.boxShadow = '';
        });

        function updateActiveFromScroll() {
            var center = carousel.scrollLeft + carousel.clientWidth / 2;
            var bestIndex = 0;
            var bestDistance = Number.POSITIVE_INFINITY;

            for (var i = 0; i < cards.length; i += 1) {
                var cardCenter = cards[i].offsetLeft + cards[i].offsetWidth / 2;
                var distance = Math.abs(cardCenter - center);
                if (distance < bestDistance) {
                    bestDistance = distance;
                    bestIndex = i;
                }
            }

            for (var j = 0; j < cards.length; j += 1) {
                cards[j].classList.toggle('active', j === bestIndex);
                cards[j].classList.remove('is-prev', 'is-next', 'is-far-left', 'is-far-right');
            }
        }

        function centerCard(index, behavior) {
            var card = cards[index];
            if (!card) return;

            var target = card.offsetLeft - (carousel.clientWidth - card.offsetWidth) / 2;
            var max = Math.max(0, carousel.scrollWidth - carousel.clientWidth);
            var left = Math.max(0, Math.min(target, max));
            carousel.scrollTo({ left: left, behavior: behavior || 'smooth' });
        }

        var scrollTimer = null;
        carousel.addEventListener('scroll', function () {
            updateActiveFromScroll();
            if (scrollTimer) clearTimeout(scrollTimer);
            scrollTimer = setTimeout(updateActiveFromScroll, 90);
        }, { passive: true });

        window.addEventListener('resize', function () {
            updateActiveFromScroll();
        }, { passive: true });

        // Keep keyboard simple: only left/right when carousel is focused/hovered.
        window.addEventListener('keydown', function (event) {
            if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;

            var isHover = carousel.matches(':hover');
            var isFocusWithin = carousel.contains(document.activeElement);
            if (!isHover && !isFocusWithin) return;

            var center = carousel.scrollLeft + carousel.clientWidth / 2;
            var current = 0;
            var bestDistance = Number.POSITIVE_INFINITY;

            for (var i = 0; i < cards.length; i += 1) {
                var cardCenter = cards[i].offsetLeft + cards[i].offsetWidth / 2;
                var distance = Math.abs(cardCenter - center);
                if (distance < bestDistance) {
                    bestDistance = distance;
                    current = i;
                }
            }

            var next = event.key === 'ArrowRight' ? Math.min(cards.length - 1, current + 1) : Math.max(0, current - 1);
            if (next !== current) {
                event.preventDefault();
                centerCard(next, 'smooth');
            }
        });

        centerCard(0, 'auto');
        updateActiveFromScroll();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
