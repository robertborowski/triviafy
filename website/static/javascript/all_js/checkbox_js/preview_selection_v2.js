// ----------------------- start -----------------------
function previewFavoriteSelection(obj){
  if ($('input[name=ui_birthday_question]:checked').length > 0) {
    var q = document.getElementById('id-birthday-question');
    if (q) q.innerHTML = document.querySelector('input[name=ui_birthday_question]:checked').value;
  }
}
// ----------------------- end -----------------------
// ----------------------- start -----------------------
function previewBirthdayMonthSelection(obj){
  if ($('input[name=ui_birthday_month]:checked').length > 0) {
    var q = document.getElementById('id-birthday-month');
    if (q) q.innerHTML = document.querySelector('input[name=ui_birthday_month]:checked').value;
  }
}
// ----------------------- end -----------------------
// ----------------------- start -----------------------
function previewBirthdayDaySelection(obj){
  if ($('input[name=ui_birthday_day]:checked').length > 0) {
    var q = document.getElementById('id-birthday-day');
    if (q) q.innerHTML = document.querySelector('input[name=ui_birthday_day]:checked').value;
  }
}
// ----------------------- end -----------------------
// ----------------------- start -----------------------
$(document).ready(function() {
  // ----------------------- remove space id names start -----------------------
  $('*').each(function() {
    var id = $(this).attr('id');
    if (id && id.includes(' ')) {
      var newId = id.replace(/\s+/g, ''); // remove any spaces from the id
      $(this).attr('id', newId); // update the id attribute value
    }
    var forId = $(this).attr('for');
    if (forId && forId.includes(' ')) {
      var newForId = forId.replace(/\s+/g, ''); // remove any spaces from the id
      $(this).attr('for', newForId); // update the id attribute value
    }
  });
  // ----------------------- remove space id names end -----------------------
  // ----------------------- checked vs unchecked classes start -----------------------
  $('input[type=checkbox][name=uiSelectedCategories]:checked').each(function() {
    var inputId = $(this).attr('id'); // get the ID of the input element
    var label = $('label[for=' + inputId + ']'); // select the associated label
    label.addClass('custom-highlight-1'); // add the custom class to the label
  });
  $('input[type=checkbox][name=uiSelectedCategories]:not(:checked)').each(function() {
    var inputId = $(this).attr('id'); // get the ID of the input element
    var label = $('label[for=' + inputId + ']'); // select the associated label
    label.removeClass('custom-highlight-1'); // add the custom class to the label
  });
});
function highlightCheckboxV1(obj){
  $('input[type=checkbox][name=uiSelectedCategories]:checked').change(function() {
    var checkboxId = $(this).prop('id');
    $('label[for=' + checkboxId + ']').addClass('custom-highlight-1');
  });
  $('input[type=checkbox][name=uiSelectedCategories]:not(:checked)').change(function() {
    var checkboxId = $(this).prop('id');
    $('label[for=' + checkboxId + ']').removeClass('custom-highlight-1');
  });
  // ----------------------- checked vs unchecked classes end -----------------------
}
// ----------------------- end -----------------------