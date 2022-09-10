// Not Signed In
const toggleButtonNotSignedIn2 = document.getElementsByClassName('toggle-button-2')[0];
const navbarLinksNotSignedIn2 = document.getElementsByClassName('navbar-links-2-not-signed-in')[0];


// JavaScript for not signed in
toggleButtonNotSignedIn2.addEventListener('click', () => {
  toggleButtonNotSignedIn2.classList.toggle('active');
  navbarLinksNotSignedIn2.classList.toggle('active');
})