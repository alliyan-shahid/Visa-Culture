/**
 * Premium horizontal-only cylindrical carousel controller.
 */
(function () {
    'use strict';

    const BASE_ANIMATION_MS = 560;
    const WHEEL_STEP_THRESHOLD = 24;
    const SWIPE_THRESHOLD_PX = 26;
    const TOUCH_INTENT_LOCK_PX = 6;
    const TOUCH_NAV_COOLDOWN_MS = 360;
    const NAV_STEP_COOLDOWN_MS = 520;

    const MIN_SECTION_VISIBLE_RATIO = 0.32;
    const CENTER_FOCUS_TOLERANCE_PX = 220;
    const ACTIVATION_COOLDOWN_MS = 180;
    const MOMENTUM_COOLDOWN_MS = 140;
    const CYLINDER_STEP_DEG = 68;
    const CYLINDER_RADIUS = 260;
    const CYLINDER_X_FACTOR = 0.95;

    const controllers = [];

    let activeController = null;
    let touchTracking = false;
    let touchStartX = 0;
    let touchStartY = 0;
    let touchStartTime = 0;
    let touchController = null;
    let touchIntentLocked = false;
    let lastActivationAt = 0;
    let lastInteractionAt = 0;
    let lastNavStepAt = 0;

    function init() {
        registerCarousels();
        if (!controllers.length) return;

        window.addEventListener('wheel', handleGlobalWheel, { passive: false });
        window.addEventListener('scroll', handleViewportState, { passive: true });
        window.addEventListener('resize', handleViewportState, { passive: true });
        window.addEventListener('keydown', handleGlobalKeydown);

        window.addEventListener('touchstart', handleTouchStart, { passive: true });
        window.addEventListener('touchmove', handleTouchMove, { passive: false });
        window.addEventListener('touchend', handleTouchEnd, { passive: true });
        window.addEventListener('touchcancel', handleTouchCancel, { passive: true });

        setupMutationObserver();
        handleViewportState();
    }

    function setupMutationObserver() {
        if (!window.MutationObserver) return;

        const observer = new MutationObserver(function () {
            registerCarousels();
            refreshAllControllers();

            if (!activeController) {
                const candidate = findBestVisibleController();
                if (candidate && isFocusReady(candidate, getSectionRect(candidate)) && canActivateNow()) {
                    setActiveController(candidate);
                }
            }
        });

        observer.observe(document.body, { childList: true, subtree: true });
    }

    function registerCarousels() {
        const tracks = document.querySelectorAll('.carousel-track');

        for (let i = 0; i < tracks.length; i += 1) {
            const track = tracks[i];
            if (findControllerByTrack(track)) continue;

            const cards = Array.from(track.querySelectorAll('.carousel-card'));
            if (!cards.length) continue;

            track.style.touchAction = 'pan-y';
            track.style.perspective = '1850px';
            track.style.transformStyle = 'preserve-3d';

            const controller = {
                section: track.closest('section') || null,
                carousel: track,
                cards: cards,
                currentIndex: 0,
                active: false,
                isAnimating: false,
                wheelDeltaAccumulator: 0,
                scrollSyncTimer: null,
                lastTouchNavAt: 0,
                animationTimer: null,
                animationFrameId: null,
                settleTimer: null
            };

            controllers.push(controller);
            attachCarouselScrollSync(controller);
            scrollToCard(controller, 0, 'auto');
        }
    }

    function attachCarouselScrollSync(controller) {
        controller.carousel.addEventListener('scroll', function () {
            if (controller.scrollSyncTimer) clearTimeout(controller.scrollSyncTimer);
            controller.scrollSyncTimer = setTimeout(function () {
                syncControllerIndexFromScroll(controller);
            }, 80);
        }, { passive: true });
    }

    function refreshAllControllers() {
        for (let i = 0; i < controllers.length; i += 1) {
            const controller = controllers[i];
            controller.cards = Array.from(controller.carousel.querySelectorAll('.carousel-card'));
            if (!controller.cards.length) continue;
            if (controller.currentIndex > controller.cards.length - 1) {
                controller.currentIndex = controller.cards.length - 1;
            }
            scrollToCard(controller, controller.currentIndex, 'auto');
        }
    }

    function findControllerByTrack(track) {
        for (let i = 0; i < controllers.length; i += 1) {
            if (controllers[i].carousel === track) return controllers[i];
        }
        return null;
    }

    function setActiveController(controller) {
        if (activeController === controller) return;
        if (activeController) deactivateController(activeController);

        activeController = controller;
        if (activeController) {
            activateController(activeController);
            lastActivationAt = Date.now();
        }
    }

    function activateController(controller) {
        controller.active = true;
        controller.wheelDeltaAccumulator = 0;
    }

    function deactivateController(controller) {
        controller.active = false;
        controller.isAnimating = false;
        controller.wheelDeltaAccumulator = 0;
        if (controller.animationFrameId) {
            cancelAnimationFrame(controller.animationFrameId);
            controller.animationFrameId = null;
        }
        if (controller.settleTimer) {
            clearTimeout(controller.settleTimer);
            controller.settleTimer = null;
        }
    }

    function lockAnimation(controller, ms) {
        controller.isAnimating = true;
        if (controller.animationTimer) clearTimeout(controller.animationTimer);
        controller.animationTimer = setTimeout(function () {
            controller.isAnimating = false;
        }, ms || BASE_ANIMATION_MS);
    }

    function getSectionRect(controller) {
        const section = controller.section || controller.carousel;
        return section.getBoundingClientRect();
    }

    function getVisibleRatio(rect) {
        const visibleTop = Math.max(rect.top, 0);
        const visibleBottom = Math.min(rect.bottom, window.innerHeight);
        const visibleHeight = Math.max(0, visibleBottom - visibleTop);
        return rect.height > 0 ? visibleHeight / rect.height : 0;
    }

    function isCenterAligned(rect) {
        const sectionCenter = rect.top + rect.height / 2;
        const viewportCenter = window.innerHeight / 2;
        const inViewport = rect.bottom > 0 && rect.top < window.innerHeight;
        return inViewport && Math.abs(sectionCenter - viewportCenter) <= CENTER_FOCUS_TOLERANCE_PX;
    }

    function isFocusReady(controller, rect) {
        if (!controller.cards.length) return false;
        if (getVisibleRatio(rect) < MIN_SECTION_VISIBLE_RATIO) return false;
        return isCenterAligned(rect);
    }

    function canActivateNow() {
        return Date.now() - lastActivationAt >= ACTIVATION_COOLDOWN_MS;
    }

    function markInteraction() {
        lastInteractionAt = Date.now();
    }

    function inNavStepCooldown() {
        return Date.now() - lastNavStepAt < NAV_STEP_COOLDOWN_MS;
    }

    function inMomentumCooldown() {
        return Date.now() - lastInteractionAt < MOMENTUM_COOLDOWN_MS;
    }

    function handleViewportState() {
        if (!controllers.length) return;

        const candidate = findBestVisibleController();
        if (!candidate) {
            if (activeController) deactivateController(activeController);
            activeController = null;
            return;
        }

        const rect = getSectionRect(candidate);
        const focusReady = isFocusReady(candidate, rect);

        if (focusReady) {
            if (canActivateNow()) setActiveController(candidate);
        } else if (activeController === candidate) {
            deactivateController(candidate);
            activeController = null;
        }
    }

    function findBestVisibleController() {
        let best = null;
        let bestDistance = Number.POSITIVE_INFINITY;

        for (let i = 0; i < controllers.length; i += 1) {
            const controller = controllers[i];
            if (!controller.cards.length) continue;

            const rect = getSectionRect(controller);
            if (!(rect.bottom > 0 && rect.top < window.innerHeight)) continue;

            const sectionCenter = rect.top + rect.height / 2;
            const viewportCenter = window.innerHeight / 2;
            const distance = Math.abs(sectionCenter - viewportCenter);

            if (distance < bestDistance) {
                best = controller;
                bestDistance = distance;
            }
        }

        return best;
    }

    function normalizeIndex(index, len) {
        return (index % len + len) % len;
    }

    function navigateBy(controller, direction, speedFactor) {
        if (!controller.cards.length) return false;
        if (inNavStepCooldown() || controller.isAnimating) return false;

        const len = controller.cards.length;
        const from = controller.currentIndex;
        const target = normalizeIndex(controller.currentIndex + direction, len);
        const duration = Math.max(320, Math.min(620, BASE_ANIMATION_MS - Math.floor((speedFactor || 0) * 120)));

        animateFocus(controller, from, target, duration);
        scrollToCard(controller, target, 'auto', 0);
        controller.currentIndex = target;
        lockAnimation(controller, duration);
        markInteraction();
        lastNavStepAt = Date.now();
        return true;
    }

    function handleGlobalWheel(event) {
        const controller = activeController;
        if (!controller || !controller.active) return;
        if (!isFocusReady(controller, getSectionRect(controller))) return;

        const useShiftWheel = !!event.shiftKey && Math.abs(event.deltaY) > 0;
        const hasHorizontalGesture = Math.abs(event.deltaX) > Math.abs(event.deltaY) && Math.abs(event.deltaX) > 0;

        if (!useShiftWheel && !hasHorizontalGesture) return;

        const delta = useShiftWheel ? event.deltaY : event.deltaX;

        event.preventDefault();
        if (controller.isAnimating || inMomentumCooldown() || inNavStepCooldown()) return;

        controller.wheelDeltaAccumulator += delta;
        if (Math.abs(controller.wheelDeltaAccumulator) < WHEEL_STEP_THRESHOLD) return;

        const direction = controller.wheelDeltaAccumulator > 0 ? 1 : -1;
        const speedFactor = Math.min(2.2, Math.abs(controller.wheelDeltaAccumulator) / 90);
        controller.wheelDeltaAccumulator = 0;

        navigateBy(controller, direction, speedFactor);
    }

    function handleGlobalKeydown(event) {
        const controller = activeController;
        if (!controller || !controller.active || controller.isAnimating) return;
        if (!isFocusReady(controller, getSectionRect(controller))) return;

        const tagName = event.target && event.target.tagName ? event.target.tagName.toLowerCase() : '';
        if (tagName === 'input' || tagName === 'textarea' || tagName === 'select' || event.target.isContentEditable) return;

        let direction = 0;
        if (event.key === 'ArrowRight') direction = 1;
        if (event.key === 'ArrowLeft') direction = -1;
        if (direction === 0) return;

        event.preventDefault();
        navigateBy(controller, direction, 0.8);
    }

    function resolveTouchController(target) {
        const track = target && target.closest ? target.closest('.carousel-track') : null;
        if (track) {
            const matched = findControllerByTrack(track);
            if (matched) return matched;
        }
        return activeController;
    }

    function handleTouchStart(event) {
        if (!event.touches || event.touches.length !== 1) return;

        const controller = resolveTouchController(event.target);
        if (!controller || !controller.active) return;
        if (!isFocusReady(controller, getSectionRect(controller))) return;

        const touch = event.touches[0];
        touchStartX = touch.clientX;
        touchStartY = touch.clientY;
        touchStartTime = Date.now();
        touchTracking = true;
        touchController = controller;
        touchIntentLocked = false;
        setActiveController(controller);
    }

    function handleTouchMove(event) {
        if (!touchTracking || !touchController || !event.touches || event.touches.length !== 1) return;
        if (touchController.isAnimating) return;

        const touch = event.touches[0];
        const dx = touch.clientX - touchStartX;
        const dy = touch.clientY - touchStartY;
        const absX = Math.abs(dx);
        const absY = Math.abs(dy);

        if (!touchIntentLocked && (absX >= TOUCH_INTENT_LOCK_PX || absY >= TOUCH_INTENT_LOCK_PX)) {
            touchIntentLocked = true;
        }

        if (touchIntentLocked && absX >= absY * 0.85) {
            event.preventDefault();
            const card = touchController.cards[touchController.currentIndex];
            const width = card ? card.offsetWidth : Math.max(1, touchController.carousel.clientWidth);
            const dragProgress = Math.max(-1, Math.min(1, -dx / Math.max(1, width)));
            renderCylindrical(touchController, touchController.currentIndex + dragProgress, false, 0);
        }
    }

    function handleTouchEnd(event) {
        const controller = touchController;

        if (!touchTracking || !controller || !controller.active || controller.isAnimating) {
            resetTouchState();
            return;
        }

        const touch = event.changedTouches && event.changedTouches[0];
        if (!touch) {
            resetTouchState();
            return;
        }

        const dx = touch.clientX - touchStartX;
        const dy = touch.clientY - touchStartY;
        const dt = Math.max(1, Date.now() - touchStartTime);
        const velocity = Math.abs(dx) / dt;
        const now = Date.now();

        resetTouchState();

        if (Math.abs(dx) <= Math.abs(dy) || Math.abs(dx) < SWIPE_THRESHOLD_PX) {
            scrollToCard(controller, controller.currentIndex, 'smooth', 340);
            renderCylindrical(controller, controller.currentIndex, true, 340);
            return;
        }

        if (now - controller.lastTouchNavAt < TOUCH_NAV_COOLDOWN_MS || inMomentumCooldown() || inNavStepCooldown()) {
            scrollToCard(controller, controller.currentIndex, 'smooth', 320);
            renderCylindrical(controller, controller.currentIndex, true, 320);
            return;
        }

        const direction = dx < 0 ? 1 : -1;
        controller.lastTouchNavAt = now;
        navigateBy(controller, direction, Math.min(2.8, velocity * 2.2));
    }

    function handleTouchCancel() {
        const controller = touchController;
        resetTouchState();

        if (controller) {
            scrollToCard(controller, controller.currentIndex, 'smooth', 300);
            renderCylindrical(controller, controller.currentIndex, true, 300);
        }
    }

    function resetTouchState() {
        touchTracking = false;
        touchController = null;
        touchIntentLocked = false;
    }

    function getShortestCircularDelta(from, to, total) {
        let delta = to - from;
        if (delta > total / 2) delta -= total;
        if (delta < -total / 2) delta += total;
        return delta;
    }

    function animateFocus(controller, fromIndex, toIndex, duration) {
        const total = controller.cards.length;
        const delta = getShortestCircularDelta(fromIndex, toIndex, total);
        const from = fromIndex;
        const to = from + delta;
        const start = performance.now();

        if (controller.animationFrameId) {
            cancelAnimationFrame(controller.animationFrameId);
            controller.animationFrameId = null;
        }

        function ease(t) {
            return 1 - Math.pow(1 - t, 3);
        }

        function tick(now) {
            const t = Math.max(0, Math.min(1, (now - start) / duration));
            const value = from + (to - from) * ease(t);
            renderCylindrical(controller, value, false, 0);

            if (t < 1) {
                controller.animationFrameId = requestAnimationFrame(tick);
                return;
            }

            controller.animationFrameId = null;
            renderCylindrical(controller, toIndex, true, 220);
            ensureCardCentered(controller, toIndex, 120);
        }

        controller.animationFrameId = requestAnimationFrame(tick);
    }

    function scrollToCard(controller, index, behavior, duration) {
        if (!controller.cards.length) return;

        const safeIndex = normalizeIndex(index, controller.cards.length);
        const card = controller.cards[safeIndex];
        const left = getCenteredScrollLeft(controller.carousel, card);

        if (behavior === 'auto') {
            controller.carousel.scrollLeft = left;
            controller.currentIndex = safeIndex;
            renderCylindrical(controller, safeIndex, true, 0);
            ensureCardCentered(controller, safeIndex, 0);
            return;
        }

        animateScrollLeft(controller.carousel, left, duration || BASE_ANIMATION_MS);
        controller.currentIndex = safeIndex;
        ensureCardCentered(controller, safeIndex, (duration || BASE_ANIMATION_MS) + 40);
    }

    function ensureCardCentered(controller, index, delayMs) {
        if (controller.settleTimer) {
            clearTimeout(controller.settleTimer);
        }

        controller.settleTimer = setTimeout(function () {
            const safeIndex = normalizeIndex(index, controller.cards.length);
            const card = controller.cards[safeIndex];
            if (!card) return;
            controller.carousel.scrollLeft = getCenteredScrollLeft(controller.carousel, card);
            controller.currentIndex = safeIndex;
            renderCylindrical(controller, safeIndex, true, 120);
        }, Math.max(0, delayMs || 0));
    }

    function animateScrollLeft(element, target, duration) {
        const start = element.scrollLeft;
        const change = target - start;
        if (Math.abs(change) < 1) {
            element.scrollLeft = target;
            return;
        }

        const startTime = performance.now();

        function ease(t) {
            return 1 - Math.pow(1 - t, 3);
        }

        function tick(now) {
            const elapsed = now - startTime;
            const t = Math.max(0, Math.min(1, elapsed / duration));
            element.scrollLeft = start + change * ease(t);
            if (t < 1) requestAnimationFrame(tick);
        }

        requestAnimationFrame(tick);
    }

    function syncControllerIndexFromScroll(controller) {
        if (!controller.cards.length) return;

        const scrollLeft = controller.carousel.scrollLeft;
        let bestIndex = controller.currentIndex;
        let bestDistance = Number.POSITIVE_INFINITY;

        for (let i = 0; i < controller.cards.length; i += 1) {
            const centeredLeft = getCenteredScrollLeft(controller.carousel, controller.cards[i]);
            const distance = Math.abs(centeredLeft - scrollLeft);
            if (distance < bestDistance) {
                bestDistance = distance;
                bestIndex = i;
            }
        }

        if (bestIndex !== controller.currentIndex) {
            controller.currentIndex = bestIndex;
        }

        renderCylindrical(controller, controller.currentIndex, true, 260);
    }

    function getCircularDelta(index, focus, total) {
        let delta = index - focus;
        delta -= Math.round(delta / total) * total;
        return delta;
    }

    function renderCylindrical(controller, focusFloat, withTransition, duration) {
        const total = controller.cards.length;
        if (!total) return;

        const transition = withTransition
            ? 'transform ' + (duration || BASE_ANIMATION_MS) + 'ms cubic-bezier(0.22, 1, 0.36, 1), opacity ' + (duration || BASE_ANIMATION_MS) + 'ms cubic-bezier(0.22, 1, 0.36, 1), filter ' + (duration || BASE_ANIMATION_MS) + 'ms cubic-bezier(0.22, 1, 0.36, 1)'
            : 'none';

        for (let i = 0; i < total; i += 1) {
            const card = controller.cards[i];
            const delta = getCircularDelta(i, focusFloat, total);
            const abs = Math.abs(delta);
            const clampedDelta = Math.max(-2.2, Math.min(2.2, delta));
            const angle = clampedDelta * CYLINDER_STEP_DEG * (Math.PI / 180);
            const x = Math.sin(angle) * CYLINDER_RADIUS * CYLINDER_X_FACTOR;
            const z = Math.cos(angle) * CYLINDER_RADIUS - CYLINDER_RADIUS;
            const rotateY = -clampedDelta * CYLINDER_STEP_DEG;
            const frontal = Math.max(0, Math.cos(angle));
            const scale = 0.82 + frontal * 0.18;
            const opacity = Math.max(0.14, Math.pow(frontal, 1.05));
            const blur = Math.max(0, abs - 0.12) * 1.2;
            const sideNarrow = 1 - Math.min(0.42, abs * 0.22);

            card.style.transition = transition;
            card.style.transform = 'translateX(' + x.toFixed(2) + 'px) translateZ(' + z.toFixed(2) + 'px) rotateY(' + rotateY.toFixed(2) + 'deg) scaleX(' + sideNarrow.toFixed(3) + ') scaleY(' + scale.toFixed(3) + ')';
            card.style.opacity = String(opacity);
            card.style.filter = 'blur(' + blur.toFixed(2) + 'px) saturate(' + (0.95 - Math.min(0.14, abs * 0.05)).toFixed(2) + ')';
            card.style.zIndex = String(120 - Math.round(abs * 20));
            card.style.border = abs < 0.6 ? '1px solid rgba(255,255,255,0.22)' : '1px solid rgba(148,163,184,0.26)';
            card.style.boxShadow = abs < 0.6
                ? '0 30px 90px rgba(15,23,42,0.34), 0 0 0 1px rgba(255,255,255,0.18) inset, 0 0 60px rgba(59,130,246,0.20)'
                : '0 14px 36px rgba(15,23,42,0.18), 0 0 0 1px rgba(255,255,255,0.08) inset';

            card.classList.toggle('active', abs < 0.5);
            card.classList.toggle('is-prev', delta < -0.5 && delta > -1.5);
            card.classList.toggle('is-next', delta > 0.5 && delta < 1.5);
            card.classList.toggle('is-far-left', delta <= -1.5);
            card.classList.toggle('is-far-right', delta >= 1.5);
        }
    }

    function getCenteredScrollLeft(carousel, card) {
        const target = card.offsetLeft - (carousel.clientWidth - card.offsetWidth) / 2;
        const max = Math.max(0, carousel.scrollWidth - carousel.clientWidth);
        return Math.max(0, Math.min(target, max));
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
