// ------------------------ start ------------------------
$(document).ready(function() {
  $('input[name="flexRadioCadence"]').change(function() {
    if ($(this).is(':checked')) {
      if ($(this).val() == 'monthly') {
        $('#flexRadioMonthly').addClass('uiSearchItemVisible');
        $('#flexRadioYearly').removeClass('uiSearchItemVisible');
      }
      if ($(this).val() == 'yearly') {
        $('#flexRadioYearly').addClass('uiSearchItemVisible');
        $('#flexRadioMonthly').removeClass('uiSearchItemVisible');
      }
    }
  });
});
// ------------------------ end ------------------------