function previewFavoriteSelection(obj){
  if ($('input[name=ui_birhday_question]:checked').length > 0) {
    var q = document.getElementById('id-birthday-question');
    if (q) q.innerHTML = document.querySelector('input[name=ui_birhday_question]:checked').value;
  }
}