let selectQuestionsButtonSection = document.getElementsByClassName('select-questions-button-section');
let selectQuestionsButtonStandInSection = document.getElementsByClassName('select-questions-button-stand-in-section');

window.onload = count_checked_checkboxes();

function count_checked_checkboxes(){
  var inputElems = document.getElementsByTagName("input"),
  // --------------------------- initialize variables start ---------------------------
  checked_counter = 0;
  unchecked_counter = 0;
  total_check_counter = 0;
  // --------------------------- initialize variables end ---------------------------
  for (var i=0; i<inputElems.length; i++) {
    // --------------------------- count all checkboxes start ---------------------------
    if (inputElems[i].type === "checkbox") {
      total_check_counter++;
    }
    // --------------------------- count all checkboxes end ---------------------------
    // --------------------------- count all unchecked checkboxes start ---------------------------
    if (inputElems[i].type === "checkbox" && inputElems[i].checked === false) {
      unchecked_counter++;
    }
    // --------------------------- count all unchecked checkboxes end ---------------------------
    // --------------------------- count all checked checkboxes start ---------------------------
    if (inputElems[i].type === "checkbox" && inputElems[i].checked === true) {
      checked_counter++;
      if (checked_counter >= 1) {
        selectQuestionsButtonSection[0].classList.add('active');
        selectQuestionsButtonStandInSection[0].classList.add('hide-mock-button');
      }
    }
    // --------------------------- count all checked checkboxes end ---------------------------
    // --------------------------- if limits start ---------------------------
    if (checked_counter <= 0 || checked_counter >= 51 || unchecked_counter === total_check_counter) {
      try {
        selectQuestionsButtonSection[0].classList.remove('active');
        selectQuestionsButtonStandInSection[0].classList.remove('hide-mock-button');
      }
      catch(err) {
        console.log('nothing')
      }
    }
    // --------------------------- if limits end ---------------------------
  }
}