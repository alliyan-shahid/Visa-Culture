/**
 * PREMIUM SCROLL ANIMATIONS
 * Advanced scroll-triggered animations for university landing pages
 */

(function () {
  'use strict';

  // Configuration
  const config = {
    threshold: 0.15,
    rootMargin: '0px 0px -100px 0px',
    animationDelay: 50, // ms between staggered items
  };

  // Initialize Intersection Observer for scroll animations
  function initScrollAnimations() {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          // Add animation to element
          entry.target.classList.add('animated');

          // Handle staggered animations for children
          const children = entry.target.querySelectorAll('[data-animation]');
          if (children.length) {
            children.forEach((child, index) => {
              setTimeout(() => {
                child.classList.add('animated');
              }, index * config.animationDelay);
            });
          }

          // Unobserve after animation
          observer.unobserve(entry.target);
        }
      });
    }, {
      threshold: config.threshold,
      rootMargin: config.rootMargin,
    });

    // Observe all animated elements
    document.querySelectorAll('[data-scroll-animation]').forEach((el) => {
      observer.observe(el);
    });

    return observer;
  }

  // Initialize counter animations
  function initCounters() {
    const counters = document.querySelectorAll('[data-counter-value]');

    const counterObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting && !entry.target.classList.contains('counted')) {
          entry.target.classList.add('counted');
          const targetValue = parseInt(entry.target.getAttribute('data-counter-value'), 10);
          const duration = parseInt(entry.target.getAttribute('data-counter-duration') || '1000', 10);

          animateCounter(entry.target, 0, targetValue, duration);
          counterObserver.unobserve(entry.target);
        }
      });
    }, {
      threshold: 0.5,
    });

    counters.forEach((counter) => {
      counterObserver.observe(counter);
    });
  }

  // Animate counter from start to end
  function animateCounter(element, start, end, duration) {
    let current = start;
    const increment = end / (duration / 16);
    const interval = setInterval(() => {
      current += increment;
      if (current >= end) {
        current = end;
        clearInterval(interval);
      }
      element.textContent = Math.floor(current).toLocaleString();
    }, 16);
  }

  // Initialize parallax scrolling
  function initParallax() {
    const parallaxElements = document.querySelectorAll('[data-parallax]');

    if (parallaxElements.length === 0) return;

    window.addEventListener('scroll', () => {
      parallaxElements.forEach((el) => {
        const scrollPosition = window.scrollY;
        const elementOffset = el.getBoundingClientRect().top + scrollPosition;
        const distance = scrollPosition - elementOffset;
        const parallaxSpeed = parseFloat(el.getAttribute('data-parallax')) || 0.5;

        el.style.transform = `translateY(${distance * parallaxSpeed}px)`;
      });
    });
  }

  // Initialize hover lift effects with mouse tracking
  function initMouseTracking() {
    const trackElements = document.querySelectorAll('[data-mouse-track]');

    trackElements.forEach((el) => {
      el.addEventListener('mousemove', (e) => {
        const rect = el.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        el.style.setProperty('--mouse-x', `${x}px`);
        el.style.setProperty('--mouse-y', `${y}px`);
      });

      el.addEventListener('mouseleave', () => {
        el.style.setProperty('--mouse-x', '50%');
        el.style.setProperty('--mouse-y', '50%');
      });
    });
  }

  // Smooth scroll to section
  function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
      anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
          target.scrollIntoView({
            behavior: 'smooth',
            block: 'start',
          });
        }
      });
    });
  }

  // Initialize text reveal animations
  function initTextReveal() {
    const textElements = document.querySelectorAll('[data-text-reveal]');

    textElements.forEach((el) => {
      const text = el.textContent;
      const words = text.split(' ');
      el.innerHTML = words
        .map((word) => {
          const chars = word.split('');
          return `<span class="word"><span class="char" style="display: inline-block;">${chars
            .map((char) => `<span class="char">${char}</span>`)
            .join('')}</span></span>`;
        })
        .join(' ');

      const chars = el.querySelectorAll('.char');
      const observer = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              chars.forEach((char, index) => {
                setTimeout(() => {
                  char.classList.add('revealed');
                }, index * 30);
              });
              observer.unobserve(el);
            }
          });
        },
        { threshold: 0.5 },
      );

      observer.observe(el);
    });
  }

  // Add CSS for text reveal if not already present
  function addTextRevealStyles() {
    if (document.querySelector('#text-reveal-styles')) return;

    const style = document.createElement('style');
    style.id = 'text-reveal-styles';
    style.textContent = `
      .char {
        opacity: 0;
        animation: characterReveal 0.5s ease forwards;
      }
      .char.revealed {
        opacity: 1;
      }
      @keyframes characterReveal {
        0% {
          opacity: 0;
          transform: translateY(20px) rotateX(90deg);
        }
        100% {
          opacity: 1;
          transform: translateY(0) rotateX(0deg);
        }
      }
    `;
    document.head.appendChild(style);
  }

  // Initialize all features
  function init() {
    initScrollAnimations();
    initCounters();
    initParallax();
    initMouseTracking();
    initSmoothScroll();
    addTextRevealStyles();
    initTextReveal();

    // Trigger animations for elements already in view
    setTimeout(() => {
      document.querySelectorAll('[data-scroll-animation]').forEach((el) => {
        if (el.getBoundingClientRect().top < window.innerHeight) {
          el.classList.add('animated');
        }
      });
    }, 100);
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // Export for manual use if needed
  window.PremiumAnimations = {
    initScrollAnimations,
    initCounters,
    initParallax,
    initMouseTracking,
    initSmoothScroll,
    initTextReveal,
  };
})();
