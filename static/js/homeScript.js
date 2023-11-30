// Smooth scrolling for navigation links
document.querySelectorAll('nav a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Intersection Observer for animations
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting && entry.intersectionRatio >= 0.1) {
            entry.target.classList.add('in-view');
        } else if (!entry.isIntersecting && entry.intersectionRatio < 0.1) {
            entry.target.classList.remove('in-view');
        }
    });
}, {
    threshold: [0, 0.1, 1] // multiple thresholds (0%, 10%, and 100%)
});

document.querySelectorAll('[data-animate]').forEach(section => {
    observer.observe(section);
});

// Initial check removed since IntersectionObserver will handle the initial check
function scrollToTop() {
     window.scrollTo({ top: 0, behavior: 'smooth' });
}