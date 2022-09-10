// Get an array of all the classes with this name. In this case all questions on the quiz will have this class
var hint_array = document.getElementsByClassName("class-check-if-hint-is-present");

// Loop through each element in the array and if there is no image present then add a class to that class, so that in CSS I can change the display to none for that combination of classes
for(var i = 0; i < hint_array.length; i++) {
  if(hint_array[i].innerHTML == 'Hint: no hint') {
    hint_array[i].className += " no-hint-present";
  }
}