let selectQuestionsButtonSection = document.getElementsByClassName('select-questions-button-section');

function count_checked_checkboxes(){
  var inputElems = document.getElementsByTagName("input"),
  checked_counter = 0;
  for (var i=0; i<inputElems.length; i++) {
  if (inputElems[i].type === "checkbox" && inputElems[i].checked === true){
    checked_counter++;
    console.log(checked_counter)
    if (checked_counter >= 10) {
      selectQuestionsButtonSection[0].classList.add('active');
    }
    if (checked_counter <= 9) {
      try {
        selectQuestionsButtonSection[0].classList.remove('active');
      }
      catch(err) {
        console.log('nothing')
      }
    }
  }
}}