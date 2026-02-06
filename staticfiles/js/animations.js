document.addEventListener('DOMContentLoaded', () => {
    // Register ScrollTrigger
    if (typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined') {
        gsap.registerPlugin(ScrollTrigger);
    } else {
        console.warn('GSAP or ScrollTrigger not loaded');
        return;
    }

    // --- SCROLL TRIGGERS ---
    // Target existing sections like the article list or dividers
    const sections = document.querySelectorAll('.editorial-divider, .section-label, .article-list');

    sections.forEach(section => {
        gsap.from(section, {
            scrollTrigger: {
                trigger: section,
                start: "top 85%",
                toggleActions: "play none none reverse"
            },
            y: 30,
            opacity: 0,
            duration: 0.6,
            ease: "power2.out"
        });
    });
});
