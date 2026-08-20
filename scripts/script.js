function loadMoreNews() {
    // Placeholder - could expand to show more posts or link to archive
    alert('More news coming soon! Check back for updates.');
}

function loadMoreProjects() {
    alert('This would load more project markdown files');
}

function loadAllMembers() {
    alert('This would load all member profiles from the members directory');
}

// JavaScript functionality for Boston Robot Hackers website

// Smooth scrolling for navigation
document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for navigation (only for anchor links)
    document.querySelectorAll('.nav-link').forEach(link => {
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
    // this just wires up manual switching and keeps the icon in sync.
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        const icon = themeToggle.querySelector('i');
        const currentTheme = () => document.documentElement.getAttribute('data-bs-theme');
        const syncIcon = () => {
            icon.className = currentTheme() === 'dark' ? 'bi bi-sun-fill' : 'bi bi-moon-stars-fill';
        };
        syncIcon();
        themeToggle.addEventListener('click', function() {
            const next = currentTheme() === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-bs-theme', next);
            localStorage.setItem('theme', next);
            syncIcon();
        });
    }
});
