// JavaScript functionality for Boston Robot Hackers website

// Smooth scrolling for navigation
document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for navigation (only for anchor links)
    document.querySelectorAll('.site-nav__link').forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            // Only prevent default for anchor links (starting with #)
            if (href.startsWith('#')) {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            }
            // Let regular links (like members.html) work normally
        });
    });

    // Clickable calendar rows: navigate to the row's announcement.
    document.querySelectorAll('.meeting-row[data-href]').forEach(row => {
        row.addEventListener('click', function() {
            window.location = this.getAttribute('data-href');
        });
    });

    // Light/dark theme toggle. The <head> inline script already set
    // data-bs-theme before paint (from localStorage or system preference);
    // this just wires up manual switching. The icon itself is two inline
    // SVGs with CSS showing whichever matches the current data-bs-theme,
    // so no JS is needed to keep it in sync.
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const next = document.documentElement.getAttribute('data-bs-theme') === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-bs-theme', next);
            localStorage.setItem('theme', next);
        });
    }
});
