// ------------------------ start ------------------------
$(document).ready(function() {
  $('input[name="flexRadioCadence"]').change(function() {
    if ($(this).is(':checked')) {
      if ($(this).val() == 'monthly') {
        // ------------------------ price 1 start ------------------------
        $('#flexRadioMonthlyPrice1').addClass('uiSearchItemVisible');
        $('#flexRadioMonthlyPrice1').removeClass('uiSearchItemInvisible');
        $('#flexRadioYearlyPrice1').addClass('uiSearchItemInvisible');
        $('#flexRadioYearlyPrice1').removeClass('uiSearchItemVisible');
        // ------------------------ price 1 end ------------------------
        // ------------------------ price 2 start ------------------------
        $('#flexRadioMonthlyPrice2').addClass('uiSearchItemVisible');
        $('#flexRadioMonthlyPrice2').removeClass('uiSearchItemInvisible');
        $('#flexRadioYearlyPrice2').addClass('uiSearchItemInvisible');
        $('#flexRadioYearlyPrice2').removeClass('uiSearchItemVisible');
        // ------------------------ price 2 end ------------------------
        // ------------------------ selection start ------------------------
        $('#flexRadioSelectMonthly').addClass('custom-bg-primary');
        $('#flexRadioSelectMonthly').addClass('fw-bold');
        $('#flexRadioSelectMonthly').addClass('custom-color-white');
        $('#flexRadioSelectYearly').removeClass('custom-bg-primary');
        $('#flexRadioSelectYearly').removeClass('fw-bold');
        $('#flexRadioSelectYearly').removeClass('custom-color-white');
        // ------------------------ selection end ------------------------
      }
      if ($(this).val() == 'yearly') {
        // ------------------------ price 1 start ------------------------
        $('#flexRadioMonthlyPrice1').addClass('uiSearchItemInvisible');
        $('#flexRadioMonthlyPrice1').removeClass('uiSearchItemVisible');
        $('#flexRadioYearlyPrice1').addClass('uiSearchItemVisible');
        $('#flexRadioYearlyPrice1').removeClass('uiSearchItemInvisible');
        // ------------------------ price 1 end ------------------------
        // ------------------------ price 2 start ------------------------
        $('#flexRadioMonthlyPrice2').addClass('uiSearchItemInvisible');
        $('#flexRadioMonthlyPrice2').removeClass('uiSearchItemVisible');
        $('#flexRadioYearlyPrice2').addClass('uiSearchItemVisible');
        $('#flexRadioYearlyPrice2').removeClass('uiSearchItemInvisible');
        // ------------------------ price 2 end ------------------------
        // ------------------------ selection start ------------------------
        $('#flexRadioSelectMonthly').removeClass('custom-bg-primary');
        $('#flexRadioSelectMonthly').removeClass('fw-bold');
        $('#flexRadioSelectMonthly').removeClass('custom-color-white');
        $('#flexRadioSelectYearly').addClass('custom-bg-primary');
        $('#flexRadioSelectYearly').addClass('fw-bold');
        $('#flexRadioSelectYearly').addClass('custom-color-white');
        // ------------------------ selection end ------------------------
      }
    }
  });
});
// ------------------------ end ------------------------