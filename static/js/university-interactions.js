
(function () {
  const reveals = document.querySelectorAll('.mel-reveal, .feature-item, .timeline-step');
  const io = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('show');
        io.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15 });
  reveals.forEach((el) => io.observe(el));

  const counters = document.querySelectorAll('.stat-counter');
  const counterIO = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting && !entry.target.classList.contains('counted')) {
        entry.target.classList.add('counted');
        const target = parseInt(entry.target.textContent.replace(/\D/g, ''), 10);
        let current = 0;
        const step = Math.max(1, Math.floor(target / 60));
        const interval = setInterval(() => {
          current += step;
          if (current >= target) {
            entry.target.textContent = entry.target.textContent;
            clearInterval(interval);
          } else {
            entry.target.textContent = `${current}${entry.target.textContent.includes('+') ? '+' : ''}`;
          }
        }, 20);
      }
    });
  }, { threshold: 0.5 });
  counters.forEach((el) => counterIO.observe(el));

  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener('click', function (e) {
      const href = this.getAttribute('href');
      if (href && href.startsWith('#') && href.length > 1 && document.querySelector(href)) {
        e.preventDefault();
        document.querySelector(href).scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });
})();
