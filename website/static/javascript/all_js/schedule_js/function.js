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

// ------------------------ start ------------------------
$("input:radio[name=radioCadence]").click(function() {
  selectedRadioCadence = $('input:radio[name=radioCadence]:checked').val();
  $("#buttonCadence").text(selectedRadioCadence);
});
// ------------------------ end ------------------------

// ===================================================================================================================================================
// Settings dropdown logic
// ------------------------ start ------------------------
window.onload = function() {
  var radios = document.querySelectorAll('input[type=radio]');
  for (var i = 0; i < radios.length; i++) {
    if (radios[i].checked) {
      // radio_candence
      selectedText = $('input:radio[name=radio_candence]:checked').val();
      $("#id-radio_candence").text(selectedText);
      // radio_start_day
      selectedText = $('input:radio[name=radio_start_day]:checked').val();
      $("#id-radio_start_day").text(selectedText);
      // radio_start_time
      selectedText = $('input:radio[name=radio_start_time]:checked').val();
      $("#id-radio_start_time").text(selectedText);
      // radio_end_day
      selectedText = $('input:radio[name=radio_end_day]:checked').val();
      $("#id-radio_end_day").text(selectedText);
      // radio_end_time
      selectedText = $('input:radio[name=radio_end_time]:checked').val();
      $("#id-radio_end_time").text(selectedText);
      // radio_timezone
      selectedText = $('input:radio[name=radio_timezone]:checked').val();
      $("#id-radio_timezone").text(selectedText);
      // radio_total_questions
      selectedText = $('input:radio[name=radio_total_questions]:checked').val();
      $("#id-radio_total_questions").text(selectedText);
      // radio_question_type
      selectedText = $('input:radio[name=radio_question_type]:checked').val();
      $("#id-radio_question_type").text(selectedText);
    }
  }
}
// radio_candence
$("input:radio[name=radio_candence]").click(function() {
  selectedText = $('input:radio[name=radio_candence]:checked').val();
  $("#id-radio_candence").text(selectedText);
});
// radio_start_day
$("input:radio[name=radio_start_day]").click(function() {
  selectedText = $('input:radio[name=radio_start_day]:checked').val();
  $("#id-radio_start_day").text(selectedText);
});
// radio_start_time
$("input:radio[name=radio_start_time]").click(function() {
  selectedText = $('input:radio[name=radio_start_time]:checked').val();
  $("#id-radio_start_time").text(selectedText);
});
// radio_end_day
$("input:radio[name=radio_end_day]").click(function() {
  selectedText = $('input:radio[name=radio_end_day]:checked').val();
  $("#id-radio_end_day").text(selectedText);
});
// radio_end_time
$("input:radio[name=radio_end_time]").click(function() {
  selectedText = $('input:radio[name=radio_end_time]:checked').val();
  $("#id-radio_end_time").text(selectedText);
});
// radio_timezone
$("input:radio[name=radio_timezone]").click(function() {
  selectedText = $('input:radio[name=radio_timezone]:checked').val();
  $("#id-radio_timezone").text(selectedText);
});
// radio_total_questions
$("input:radio[name=radio_total_questions]").click(function() {
  selectedText = $('input:radio[name=radio_total_questions]:checked').val();
  $("#id-radio_total_questions").text(selectedText);
});
// radio_question_type
$("input:radio[name=radio_question_type]").click(function() {
  selectedText = $('input:radio[name=radio_question_type]:checked').val();
  $("#id-radio_question_type").text(selectedText);
});
// ------------------------ end ------------------------