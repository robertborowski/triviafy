let selectQuestionsButtonSection = document.getElementsByClassName('select-questions-button-section');
let selectQuestionsButtonStandInSection = document.getElementsByClassName('select-questions-button-stand-in-section');

window.onload = count_checked_checkboxes();

function count_checked_checkboxes(){
  var inputElems = document.getElementsByTagName("input"),
  checked_counter = 0;
  for (var i=0; i<inputElems.length; i++) {
    if (inputElems[i].type === "checkbox" && inputElems[i].checked === true) {
      checked_counter++;
      // console.log(checked_counter)
      if (checked_counter == 10) {
        selectQuestionsButtonSection[0].classList.add('active');
        selectQuestionsButtonStandInSection[0].classList.add('hide-mock-button');
      }
      if (checked_counter <= 9 || checked_counter >= 11) {
        try {
          selectQuestionsButtonSection[0].classList.remove('active');
          selectQuestionsButtonStandInSection[0].classList.remove('hide-mock-button');
        }
        catch(err) {
          console.log('nothing')
        }
      }
    }
  }
}