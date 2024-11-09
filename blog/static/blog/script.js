// script.js

document.addEventListener('DOMContentLoaded', () => {
  const menuIcon = document.getElementById('menu-icon');
  const menu = document.querySelector('.menu');
  // when user press menu icon
  menuIcon.addEventListener('click', () => {
    menu.classList.toggle('show');
    // Modify the SVG content to display a cross
    // Toggle the 'open' class on the menu-icon
    menuIcon.classList.toggle('open');
  });
});
