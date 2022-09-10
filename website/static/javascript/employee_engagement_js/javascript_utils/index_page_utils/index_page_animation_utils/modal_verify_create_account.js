// Get modal element
var createAccountModalDetails = document.getElementById('create-account-details-modal');
// Get open modal button
var createAccountActivateModal = document.getElementById('create-account-activate-modal');
// Get open modal button
var closeCreateAccountModalXButton = document.getElementsByClassName('close-create-account-modal-x-button')[0];



// Listen for open click
createAccountActivateModal.addEventListener('click', openModal);
// Listen for open click
closeCreateAccountModalXButton.addEventListener('click', closeModal);
// Listen for outside click
window.addEventListener('click', outsideClick);



// Function to open modal
function openModal(){
  createAccountModalDetails.style.display = 'block';
}

// Function to close modal
function closeModal(){
  createAccountModalDetails.style.display = 'none';
}

// Function to close modal if outside click
function outsideClick(e){
  if(e.target == createAccountModalDetails){
    createAccountModalDetails.style.display = 'none';
  }
}