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
        $('#flexRadioSelectMonthly').addClass('custom-bg-color-1');
        $('#flexRadioSelectMonthly').addClass('fw-bold');
        $('#flexRadioSelectMonthly').addClass('custom-color-4');
        $('#flexRadioSelectMonthly').removeClass('custom-img-opacity-3');
        $('#flexRadioSelectYearly').removeClass('custom-bg-color-1');
        $('#flexRadioSelectYearly').removeClass('fw-bold');
        $('#flexRadioSelectYearly').removeClass('custom-color-4');
        $('#flexRadioSelectYearly').addClass('custom-img-opacity-3');
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
        $('#flexRadioSelectMonthly').removeClass('custom-bg-color-1');
        $('#flexRadioSelectMonthly').removeClass('fw-bold');
        $('#flexRadioSelectMonthly').removeClass('custom-color-4');
        $('#flexRadioSelectMonthly').addClass('custom-img-opacity-3');
        $('#flexRadioSelectYearly').addClass('custom-bg-color-1');
        $('#flexRadioSelectYearly').addClass('fw-bold');
        $('#flexRadioSelectYearly').addClass('custom-color-4');
        $('#flexRadioSelectYearly').removeClass('custom-img-opacity-3');
        // ------------------------ selection end ------------------------
      }
    }
  });
});
// ------------------------ end ------------------------