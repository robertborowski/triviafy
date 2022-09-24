// Not Signed In
const toggleButtonNotSignedIn4 = document.getElementsByClassName('toggle-button-4')[0];
const navbarLinksNotSignedIn4 = document.getElementsByClassName('navbar-links-4-signed-in')[0];


// JavaScript for not signed in
toggleButtonNotSignedIn4.addEventListener('click', () => {
  toggleButtonNotSignedIn4.classList.toggle('active');
  navbarLinksNotSignedIn4.classList.toggle('active');
})