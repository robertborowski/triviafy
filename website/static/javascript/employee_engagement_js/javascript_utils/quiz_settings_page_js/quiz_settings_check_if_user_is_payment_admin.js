var section_quiz_settings_edit_button = document.getElementsByClassName("quiz-settings-edit-section");
var user_payment_admin = document.getElementById("quiz-settings-if-payment-admin");

console.log('- - - - - - -');
console.log(user_payment_admin.innerHTML);
console.log(section_quiz_settings_edit_button[0])
console.log('- - - - - - -');


if(user_payment_admin.innerHTML == 'True') {
  section_quiz_settings_edit_button[0].className += " show-edit-button";
}