document.addEventListener("DOMContentLoaded", function() {
    var loadingScreen = document.getElementById('loading-screen');
    var minDisplayTime = 600; // Minimum display time in milliseconds
    var startTime;

    function showLoadingScreen() {
        startTime = Date.now();
        loadingScreen.classList.add('visible');
        requestAnimationFrame(() => {
            loadingScreen.style.opacity = '1'; // Ensure the opacity transition
        });
    }

    function hideLoadingScreen() {
        var elapsedTime = Date.now() - startTime;
        var remainingTime = minDisplayTime - elapsedTime;

        if (remainingTime > 0) {
            setTimeout(function() {
                loadingScreen.style.opacity = '0'; // Fade out
                setTimeout(() => {
                    loadingScreen.classList.remove('visible');
                }, 200); // Match the transition duration
            }, remainingTime);
        } else {
            loadingScreen.style.opacity = '0'; // Fade out
            setTimeout(() => {
                loadingScreen.classList.remove('visible');
            }, 200); // Match the transition duration
        }
    }

    function handleLinkClick(event) {
        var link = event.currentTarget;
        var href = link.getAttribute('href');
        if (href && href !== '#') {
            event.preventDefault();
            showLoadingScreen();
            setTimeout(function() {
                window.location.href = href;
            }, 10); // Minimal delay to ensure loading screen is visible
        }
    }

    // Attach click event to all links
    document.querySelectorAll('a').forEach(function(link) {
        link.addEventListener('click', handleLinkClick);
    });

    // Show loading screen on initial load
    showLoadingScreen();
    window.addEventListener('load', function() {
        hideLoadingScreen();
    });

    // Hide loading screen on back/forward navigation
    window.addEventListener('popstate', function() {
        hideLoadingScreen();
    });
});
