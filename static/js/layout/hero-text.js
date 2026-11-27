        try {
            const heroText = document.getElementById('hero-text');
            const heroLines = heroText ? Array.from(heroText.querySelectorAll('.hero-line')) : [];
            if (heroLines.length) {
                const fadeOut = () => heroLines.forEach(line => { line.classList.remove('line-hidden'); line.classList.add('line-fadeout'); });
                const revealSequence = () => {
                    heroLines.forEach(line => { line.classList.remove('line-fadeout'); line.classList.add('line-hidden'); });
                    setTimeout(() => heroLines[0]?.classList.remove('line-hidden'), 1000);
                    setTimeout(() => heroLines[1]?.classList.remove('line-hidden'), 2000);
                    setTimeout(() => heroLines[2]?.classList.remove('line-hidden'), 3000);
                };
                const runHeroLoop = () => { fadeOut(); setTimeout(revealSequence, 800); };
                setTimeout(() => { runHeroLoop(); setInterval(runHeroLoop, 10000); }, 5000);
            }
        } catch (e) { console.warn('hero animation failed', e); }

