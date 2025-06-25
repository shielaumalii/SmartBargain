document.addEventListener('DOMContentLoaded', () => {
  const navLinks = [
    { id: 'link-home', url: 'homepage.html' },
    { id: 'link-products', url: 'products.html' },
    { id: 'link-negotiate', url: 'negotiate.html' },
    { id: 'link-dashboard', url: 'dashboard.html' },
    { id: 'link-login', url: 'login.html' }
  ];

  navLinks.forEach(link => {
    const el = document.getElementById(link.id);
    if (el) {
      el.addEventListener('click', function(e) {
        e.preventDefault();
        window.location.href = link.url;
      });
    }
  });
});
