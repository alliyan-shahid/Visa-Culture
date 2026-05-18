/**
 * Ideas section full-page scroll lock controller.
 * Activates when section center reaches viewport center.
 * While active, wheel scrolling anywhere on page controls card transitions.
 */
(function () {
    'use strict';

    const ANIMATION_LOCK_MS = 700;
    const ACTIVATION_TOLERANCE_PX = 120;
    const MICRO_SCROLL_THRESHOLD = 8;

    let section = null;
    let carousel = null;
    let cards = [];

    let active = false;
    let currentIndex = 0;
    let isAnimating = false;
    let wasBodyOverflow = '';
    let requireCenterExitBeforeRelock = false;
    let isSnappingToCenter = false;

    function init() {
        section = document.getElementById('ideaCarouselSection');
        carousel = document.getElementById('ideaCarousel');
        if (!section || !carousel) return;

        cards = Array.from(carousel.querySelectorAll('.carousel-card'));
        if (!cards.length) return;

        scrollToCard(0, 'auto');

        window.addEventListener('wheel', handleGlobalWheel, { passive: false });
        window.addEventListener('scroll', handleViewportState, { passive: true });
        window.addEventListener('resize', handleViewportState, { passive: true });

        handleViewportState();
    }

    function handleViewportState() {
        if (!section) return;

        const rect = section.getBoundingClientRect();
        const sectionCenter = rect.top + rect.height / 2;
        const viewportCenter = window.innerHeight / 2;
        const centerAligned = Math.abs(sectionCenter - viewportCenter) <= ACTIVATION_TOLERANCE_PX;
        const inViewport = rect.bottom > 0 && rect.top < window.innerHeight;

        if (!centerAligned) {
            requireCenterExitBeforeRelock = false;
        }

        if (centerAligned && inViewport) {
            if (requireCenterExitBeforeRelock) return;
            activateIdeasScroll(rect);
            return;
        }

        if (!centerAligned && active) {
            deactivateIdeasScroll();
        }
    }

    function activateIdeasScroll(rect) {
        if (active) return;
        active = true;
        wasBodyOverflow = document.body.style.overflow;
        document.body.style.overflow = 'hidden';
        snapSectionToViewportCenter(rect);
    }

    function deactivateIdeasScroll() {
        if (!active) return;
        active = false;
        document.body.style.overflow = wasBodyOverflow || '';
        isAnimating = false;
    }

    function lockAnimation() {
        isAnimating = true;
        setTimeout(function () {
            isAnimating = false;
        }, ANIMATION_LOCK_MS);
    }

    function snapSectionToViewportCenter(existingRect) {
        const rect = existingRect || section.getBoundingClientRect();
        const sectionCenter = rect.top + rect.height / 2;
        const viewportCenter = window.innerHeight / 2;
        const offset = sectionCenter - viewportCenter;

        if (Math.abs(offset) < 1) return;

        isSnappingToCenter = true;
        window.scrollBy({ top: offset, behavior: 'smooth' });
        setTimeout(function () {
            isSnappingToCenter = false;
        }, 320);
    }

    function atFirstCard() {
        return currentIndex <= 0;
    }

    function atLastCard() {
        return currentIndex >= cards.length - 1;
    }

    function moveNextCard() {
        if (atLastCard()) return false;
        currentIndex += 1;
        scrollToCard(currentIndex);
        return true;
    }

    function movePreviousCard() {
        if (atFirstCard()) return false;
        currentIndex -= 1;
        scrollToCard(currentIndex);
        return true;
    }

    function unlockForBoundary(direction) {
        requireCenterExitBeforeRelock = true;
        deactivateIdeasScroll();
        if (direction > 0) {
            window.scrollBy(0, 2);
        } else {
            window.scrollBy(0, -2);
        }
    }

    function handleGlobalWheel(event) {
        const deltaY = event.deltaY || 0;
        if (!active) return;

        event.preventDefault();

        console.log({
            active: active,
            currentIndex: currentIndex,
            deltaY: deltaY,
            isAnimating: isAnimating,
            bodyOverflow: document.body.style.overflow
        });

        if (isSnappingToCenter || isAnimating || deltaY === 0) return;
        if (Math.abs(deltaY) < MICRO_SCROLL_THRESHOLD) return;

        if (deltaY > 0) {
            if (atLastCard()) {
                unlockForBoundary(1);
                return;
            }
            if (moveNextCard()) {
                lockAnimation();
            }
            return;
        }

        if (deltaY < 0) {
            if (atFirstCard()) {
                unlockForBoundary(-1);
                return;
            }
            if (movePreviousCard()) {
                lockAnimation();
            }
        }
    }

    function scrollToCard(index, behavior) {
        const safeIndex = Math.max(0, Math.min(cards.length - 1, index));
        currentIndex = safeIndex;

        const card = cards[safeIndex];
        const left = card.offsetLeft - (carousel.clientWidth - card.clientWidth) / 2;

        carousel.scrollTo({
            left: left,
            behavior: behavior || 'smooth'
        });

        updateActiveClass();
    }

    function updateActiveClass() {
        for (let i = 0; i < cards.length; i += 1) {
            const card = cards[i];
            const offset = i - currentIndex;

            card.classList.toggle('active', offset === 0);
            card.classList.toggle('is-prev', offset === -1);
            card.classList.toggle('is-next', offset === 1);
            card.classList.toggle('is-far-left', offset < -1);
            card.classList.toggle('is-far-right', offset > 1);
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
