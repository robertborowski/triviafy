// Not Signed In
const toggleButtonNotSignedIn3 = document.getElementsByClassName('toggle-button-3')[0];
const navbarLinksNotSignedIn3 = document.getElementsByClassName('navbar-links-3-not-signed-in')[0];


// JavaScript for not signed in
toggleButtonNotSignedIn3.addEventListener('click', () => {
  toggleButtonNotSignedIn3.classList.toggle('active');
  navbarLinksNotSignedIn3.classList.toggle('active');
})