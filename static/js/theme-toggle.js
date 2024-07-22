document.addEventListener('DOMContentLoaded', (event) => {
    const themeToggle = document.getElementById('theme-toggle');
    const avatar = document.getElementById('avatar');

    // Avatar URLs for different themes
    const avatarUrls = {
       'default': 'https://cdn.iconscout.com/icon/free/png-256/free-ironman-marvel-super-hero-earth-saver-avenger-28699.png?f=webp',
        'cool-blue': 'https://avatars.githubusercontent.com/u/4596389?v=4',
        'nature-green': 'https://www.vectorkhazana.com/assets/images/products/Lego_Hulk_Face.png',
        'forest': 'https://tr.rbxcdn.com/1072e2b7f22e2d3e1629d8af47323d70/420/420/Image/Png'
    };

    // Function to update the avatar based on the theme
    function updateAvatar(theme) {
        if (avatar) {
            avatar.src = avatarUrls[theme] || avatarUrls['default'];
        }
    }

    // Apply the saved theme and avatar on page load
    const savedTheme = localStorage.getItem('theme') || 'default';
    document.body.classList.add(`${savedTheme}-theme`);
    if (themeToggle) {
        themeToggle.value = savedTheme;
    }
    updateAvatar(savedTheme);

    // Change theme and update avatar when the theme is changed
    if (themeToggle) {
        themeToggle.addEventListener('change', () => {
            document.body.classList.remove('default-theme', 'cool-blue-theme', 'nature-green-theme', 'forest-theme');
            const selectedTheme = themeToggle.value;
            document.body.classList.add(`${selectedTheme}-theme`);
            // Save the selected theme to localStorage
            localStorage.setItem('theme', selectedTheme);
            // Update the avatar
            updateAvatar(selectedTheme);
        });
    }
});
