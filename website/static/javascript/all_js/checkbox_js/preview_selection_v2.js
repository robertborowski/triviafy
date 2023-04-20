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