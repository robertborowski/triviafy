// ------------------------ start ------------------------
$("input:radio[name=radioStartDay]").click(function() {
  selectedRadioStartDay = $('input:radio[name=radioStartDay]:checked').val();
  $("#buttonStartDay").text(selectedRadioStartDay);
});
// ------------------------ end ------------------------

// ------------------------ start ------------------------
$("input:radio[name=radioStartTime]").click(function() {
  selectedRadioStartTime = $('input:radio[name=radioStartTime]:checked').val();
  $("#buttonStartTime").text(selectedRadioStartTime);
});
// ------------------------ end ------------------------

// ------------------------ start ------------------------
$("input:radio[name=radioEndDay]").click(function() {
  selectedRadioEndDay = $('input:radio[name=radioEndDay]:checked').val();
  $("#buttonEndDay").text(selectedRadioEndDay);
});
// ------------------------ end ------------------------

// ------------------------ start ------------------------
$("input:radio[name=radioEndTime]").click(function() {
  selectedRadioEndTime = $('input:radio[name=radioEndTime]:checked').val();
  $("#buttonEndTime").text(selectedRadioEndTime);
});
// ------------------------ end ------------------------

// ------------------------ start ------------------------
$("input:radio[name=radioTimeZone]").click(function() {
  selectedRadioTimeZone = $('input:radio[name=radioTimeZone]:checked').val();
  $("#buttonTimeZone").text(selectedRadioTimeZone);
});
// ------------------------ end ------------------------

// ------------------------ start ------------------------
$("input:radio[name=radioTotalQuestions]").click(function() {
  selectedRadioTotalQuestions = $('input:radio[name=radioTotalQuestions]:checked').val();
  $("#buttonTotalQuestions").text(selectedRadioTotalQuestions);
});
// ------------------------ end ------------------------

// ------------------------ start ------------------------
$("input:radio[name=radioQuestionType]").click(function() {
  selectedRadioQuestionType = $('input:radio[name=radioQuestionType]:checked').val();
  $("#buttonQuestionType").text(selectedRadioQuestionType);
});
// ------------------------ end ------------------------