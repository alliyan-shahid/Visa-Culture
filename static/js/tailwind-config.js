window.tailwind = window.tailwind || {};
window.tailwind.config = {
    theme: {
        extend: {
            fontFamily: {
                sans: ['Manrope', 'sans-serif'],
                display: ['Playfair Display', 'serif'],
            },
            colors: {
                primary: '#0a4d8f',
                accent: '#0d9488',
                luxe: '#c49a3a',
                surface: '#f5f7fb',
                muted: '#556277',
                card: '#ffffff'
            },
            boxShadow: {
                soft: '0 24px 80px rgba(15, 23, 42, 0.08)',
                softmd: '0 18px 60px rgba(15, 23, 42, 0.08)'
            },
            borderRadius: {
                '4xl': '2rem'
            }
        }
    }
};
