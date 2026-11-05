// JavaScript functionality for Boston Robot Hackers website

document.addEventListener('DOMContentLoaded', function() {
    // Light/dark theme toggle. The <head> inline script already set
    // data-theme before paint (from localStorage or system preference);
    // this just wires up manual switching. The icon itself is two inline
    // SVGs with CSS showing whichever matches the current data-theme,
    // so no JS is needed to keep it in sync.
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const next = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', next);
            localStorage.setItem('theme', next);
        });
    }
});
