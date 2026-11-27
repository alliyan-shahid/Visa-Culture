        try {
            const revealObserver = new IntersectionObserver((entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('is-visible');
                        revealObserver.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.18 });

            document.querySelectorAll('.reveal, .reveal-fade').forEach((el) => revealObserver.observe(el));
            document.querySelectorAll('.reveal, .reveal-fade').forEach((el) => {
                const rect = el.getBoundingClientRect();
                if (rect.top < window.innerHeight && rect.bottom > 0) el.classList.add('is-visible');
            });
        } catch (err) {
            console.warn('reveal observer failed', err);
            document.querySelectorAll('.reveal, .reveal-fade').forEach((el) => el.classList.add('is-visible'));
        }

