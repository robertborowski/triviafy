// Get modal element
var loginModalDetails = document.getElementById('login-details-modal');
// Get open modal button
var loginActivateModal = document.getElementById('login-activate-modal');
// Get open modal button
var closeLoginModalXButton = document.getElementsByClassName('close-login-modal-x-button')[0];



// Listen for open click
loginActivateModal.addEventListener('click', openModal);
// Listen for open click
closeLoginModalXButton.addEventListener('click', closeModal);
// Listen for outside click
window.addEventListener('click', outsideClick);



// Function to open modal
function openModal(){
  loginModalDetails.style.display = 'block';
}

// Function to close modal
function closeModal(){
  loginModalDetails.style.display = 'none';
}

// Function to close modal if outside click
function outsideClick(e){
  if(e.target == loginModalDetails){
    loginModalDetails.style.display = 'none';
  }
}