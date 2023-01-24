function previewSelectionDate(obj){
  if ($('input[name=uiDateSelected]:checked').length > 0) {
    var q = document.getElementById('placeholder-date');
    if (q) q.innerHTML = document.querySelector('input[name=uiDateSelected]:checked').value;
  }
}

function previewSelectionTime(obj){
  if ($('input[name=uiTimeSelected]:checked').length > 0) {
    var q = document.getElementById('placeholder-time');
    if (q) q.innerHTML = document.querySelector('input[name=uiTimeSelected]:checked').value;
  }
}

function previewSelectionTimeZone(obj){
  if ($('input[name=uiTimeZoneSelected]:checked').length > 0) {
    var q = document.getElementById('placeholder-timezone');
    if (q) q.innerHTML = document.querySelector('input[name=uiTimeZoneSelected]:checked').value;
  }
}