// Cambiar navbar al hacer scroll
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.classList.add('navbar-scrolled', 'bg-black');
        navbar.classList.remove('bg-dark');
    } else {
        navbar.classList.remove('navbar-scrolled', 'bg-black');
        navbar.classList.add('bg-dark');
    }
});
