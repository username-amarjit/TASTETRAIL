tailwind.config = {
    darkMode: 'class',
    theme: {
        extend: {
            colors: {
                dark: {
                    bg: '#1a202c',
                    text: '#e2e8f0',
                },
            },
        },
    },
}


const menuToggle = document.getElementById('menuToggle');
const menu = document.getElementById('menu');

if(menuToggle) {menuToggle.addEventListener('click', () => {
    menu.classList.toggle('hidden');
    menu.style.transition = 'max-height 0.3s ease-in-out';
    menu.style.maxHeight = menu.classList.contains('hidden') ? '0' : menu.scrollHeight + 'px';
});
}
window.addEventListener('resize', () => {
    if (window.innerWidth >= 1024) {
        menu.classList.remove('hidden');
        menu.style.maxHeight = 'none';
    } else {
        menu.classList.add('hidden');
        menu.style.maxHeight = '0';
    }
});


        // Toggle dark mode
function toggleDarkMode() {
    document.documentElement.classList.toggle('dark');    
}


// Add dark mode toggle button
const darkModeToggle = document.querySelector('#themeModeToggle');
darkModeToggle.addEventListener('click', toggleDarkMode);