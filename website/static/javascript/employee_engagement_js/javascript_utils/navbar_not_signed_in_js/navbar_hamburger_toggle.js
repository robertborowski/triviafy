// Not Signed In
const toggleButtonNotSignedIn = document.getElementsByClassName('toggle-button-not-signed-in')[0];
const navbarLinksNotSignedIn = document.getElementsByClassName('navbar-links-not-signed-in')[0];


// JavaScript for not signed in
toggleButtonNotSignedIn.addEventListener('click', () => {
  toggleButtonNotSignedIn.classList.toggle('active');
  navbarLinksNotSignedIn.classList.toggle('active');
})