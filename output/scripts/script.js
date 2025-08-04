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

// Theme switching removed - themes are now build-time only

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
});