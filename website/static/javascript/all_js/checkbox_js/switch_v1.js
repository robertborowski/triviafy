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
        // ------------------------ subscription section 1 start ------------------------
        $('#flexRadioSectionMonthly1').addClass('uiSearchItemVisible');
        $('#flexRadioSectionMonthly1').removeClass('uiSearchItemInvisible');
        $('#flexRadioSectionYearly1').addClass('uiSearchItemInvisible');
        $('#flexRadioSectionYearly1').removeClass('uiSearchItemVisible');
        // ------------------------ subscription section 1 end ------------------------
        // ------------------------ subscription section 2 start ------------------------
        $('#flexRadioSectionMonthly2').addClass('uiSearchItemVisible');
        $('#flexRadioSectionMonthly2').removeClass('uiSearchItemInvisible');
        $('#flexRadioSectionYearly2').addClass('uiSearchItemInvisible');
        $('#flexRadioSectionYearly2').removeClass('uiSearchItemVisible');
        // ------------------------ subscription section 2 end ------------------------
        // ------------------------ subscription 1 start ------------------------
        $('#flexRadioMonthlySubscription1').addClass('uiSearchItemVisible');
        $('#flexRadioMonthlySubscription1').removeClass('uiSearchItemInvisible');
        $('#flexRadioYearlySubscription1').addClass('uiSearchItemInvisible');
        $('#flexRadioYearlySubscription1').removeClass('uiSearchItemVisible');
        // ------------------------ subscription 1 end ------------------------
        // ------------------------ subscription 2 start ------------------------
        $('#flexRadioMonthlySubscription2').addClass('uiSearchItemVisible');
        $('#flexRadioMonthlySubscription2').removeClass('uiSearchItemInvisible');
        $('#flexRadioYearlySubscription2').addClass('uiSearchItemInvisible');
        $('#flexRadioYearlySubscription2').removeClass('uiSearchItemVisible');
        // ------------------------ subscription 2 end ------------------------
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
        // ------------------------ subscription section 1 start ------------------------
        $('#flexRadioSectionYearly1').addClass('uiSearchItemVisible');
        $('#flexRadioSectionYearly1').removeClass('uiSearchItemInvisible');
        $('#flexRadioSectionMonthly1').addClass('uiSearchItemInvisible');
        $('#flexRadioSectionMonthly1').removeClass('uiSearchItemVisible');
        // ------------------------ subscription section 1 end ------------------------
        // ------------------------ subscription section 1 start ------------------------
        $('#flexRadioSectionYearly2').addClass('uiSearchItemVisible');
        $('#flexRadioSectionYearly2').removeClass('uiSearchItemInvisible');
        $('#flexRadioSectionMonthly2').addClass('uiSearchItemInvisible');
        $('#flexRadioSectionMonthly2').removeClass('uiSearchItemVisible');
        // ------------------------ subscription section 1 end ------------------------
        // ------------------------ subscription 1 start ------------------------
        $('#flexRadioMonthlySubscription1').addClass('uiSearchItemInvisible');
        $('#flexRadioMonthlySubscription1').removeClass('uiSearchItemVisible');
        $('#flexRadioYearlySubscription1').addClass('uiSearchItemVisible');
        $('#flexRadioYearlySubscription1').removeClass('uiSearchItemInvisible');
        // ------------------------ subscription 1 end ------------------------
        // ------------------------ subscription 2 start ------------------------
        $('#flexRadioMonthlySubscription2').addClass('uiSearchItemInvisible');
        $('#flexRadioMonthlySubscription2').removeClass('uiSearchItemVisible');
        $('#flexRadioYearlySubscription2').addClass('uiSearchItemVisible');
        $('#flexRadioYearlySubscription2').removeClass('uiSearchItemInvisible');
        // ------------------------ subscription 2 end ------------------------
      }
    }
  });
});
// ------------------------ end ------------------------