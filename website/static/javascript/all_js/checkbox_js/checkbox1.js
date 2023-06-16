function handleCheckboxChange() {
    var checkbox = document.getElementById("id-flexCheckDefault");
    var userEmail = document.getElementById("id-user_email");
    
    if (checkbox.checked) {
      userEmail.classList.add("custom-blur-1");
      userEmail.classList.add("custom-transition-1");
    } else {
      userEmail.classList.remove("custom-blur-1");
      userEmail.classList.remove("custom-transition-1");
    }
  }