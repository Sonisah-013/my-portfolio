/**
 * Soni Sah Portfolio - Main Interactivity Logic
 */

document.addEventListener('DOMContentLoaded', () => {
    
    // 1. Navbar Scroll Effect
    // Adds a shadow and background blur as you scroll down
    const navbar = document.querySelector('.topnav');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.style.background = 'rgba(2, 6, 23, 0.95)';
            navbar.style.boxShadow = '0 10px 30px -10px rgba(0,0,0,0.5)';
        } else {
            navbar.style.background = 'rgba(2, 6, 23, 0.8)';
            navbar.style.boxShadow = 'none';
        }
    });

    // 2. Typing Effect for Hero Section
    // Only runs if the element with id "typewriter" exists (usually on Home page)
    const typeTarget = document.getElementById('typewriter');
    if (typeTarget) {
        const phrases = [
            "Neural Networks.",
            "Scalable Django APIs.",
            "Predictive Models.",
            "RAG-based Systems."
        ];
        let i = 0;
        let j = 0;
        let currentPhrase = [];
        let isDeleting = false;
        let isEnd = false;

        function loop() {
            isEnd = false;
            typeTarget.innerHTML = currentPhrase.join('');

            if (i < phrases.length) {
                if (!isDeleting && j <= phrases[i].length) {
                    currentPhrase.push(phrases[i][j]);
                    j++;
                }

                if (isDeleting && j <= phrases[i].length) {
                    currentPhrase.pop(phrases[i][j]);
                    j--;
                }

                if (j == phrases[i].length) {
                    isEnd = true;
                    isDeleting = true;
                }

                if (isDeleting && j === 0) {
                    currentPhrase = [];
                    isDeleting = false;
                    i++;
                    if (i === phrases.length) i = 0;
                }
            }
            const spedUp = Math.random() * (80 - 50) + 50;
            const normalSpeed = Math.random() * (150 - 100) + 100;
            const time = isEnd ? 2000 : isDeleting ? spedUp : normalSpeed;
            setTimeout(loop, time);
        }
        loop();
    }

    // 3. Reveal on Scroll Animation
    // Automatically triggers animations when elements enter the viewport
    const observerOptions = {
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                observer.unobserve(entry.target); // Run animation once
            }
        });
    }, observerOptions);

    // Apply reveal effect to all cards and headers
    document.querySelectorAll('.card, section h1, section h2').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'all 0.8s ease-out';
        observer.observe(el);
    });

    // 4. Contact Form Loading State
    const contactForm = document.querySelector('form');
    if (contactForm) {
        contactForm.addEventListener('submit', () => {
            const btn = contactForm.querySelector('button');
            btn.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Sending...';
            btn.style.opacity = '0.7';
            btn.style.pointerEvents = 'none';
        });
    }

    // 5. Smooth Scroll for Anchor Links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
});