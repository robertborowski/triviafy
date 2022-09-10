// Get an array of all the classes with this name. In this case all questions on the quiz will have this class
var user_submitted_quiz_answers_arr = document.getElementsByClassName("user-subitted-quiz-answers");
var user_answers_submitted_message_section = document.getElementsByClassName("user-answers-submitted-message-section");


// Check the value of the class name element and if meets criteria then make the change to display
if(user_submitted_quiz_answers_arr[0].innerHTML != '') {
  user_answers_submitted_message_section[0].style.display="block";
}