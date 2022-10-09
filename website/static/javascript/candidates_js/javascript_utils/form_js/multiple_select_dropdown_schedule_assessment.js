// -------------- 1 start --------------
var checkListAssessment = document.getElementById('js-schedule-list-assessment-names');
checkListAssessment.getElementsByClassName('schedule-anchor-span-assessment-names')[0].onclick = function(evt) {
  if (checkListAssessment.classList.contains('visible'))
    checkListAssessment.classList.remove('visible');
  else
    checkListAssessment.classList.add('visible');
    // -------------- Turn off others start --------------
    if (checkListCandidate.classList.contains('visible'))
      checkListCandidate.classList.remove('visible');
    if (checkListDate.classList.contains('visible'))
      checkListDate.classList.remove('visible');
    if (checkListTime.classList.contains('visible'))
      checkListTime.classList.remove('visible');
    // -------------- Turn off others end --------------
}
// -------------- 1 end --------------

// -------------- 2 start --------------
var checkListCandidate = document.getElementById('js-schedule-list-candidate-names');
checkListCandidate.getElementsByClassName('schedule-anchor-span-candidate-names')[0].onclick = function(evt) {
  if (checkListCandidate.classList.contains('visible'))
    checkListCandidate.classList.remove('visible');
  else
    checkListCandidate.classList.add('visible');
    // -------------- Turn off others start --------------
    if (checkListAssessment.classList.contains('visible'))
      checkListAssessment.classList.remove('visible');
    if (checkListDate.classList.contains('visible'))
      checkListDate.classList.remove('visible');
    if (checkListTime.classList.contains('visible'))
      checkListTime.classList.remove('visible');
    // -------------- Turn off others end --------------
}
// -------------- 2 end --------------

// -------------- 3 start --------------
var checkListDate = document.getElementById('js-schedule-list-date');
checkListDate.getElementsByClassName('schedule-anchor-span-date')[0].onclick = function(evt) {
  if (checkListDate.classList.contains('visible'))
    checkListDate.classList.remove('visible');
  else
    checkListDate.classList.add('visible');
    // -------------- Turn off others start --------------
    if (checkListAssessment.classList.contains('visible'))
      checkListAssessment.classList.remove('visible');
    if (checkListCandidate.classList.contains('visible'))
      checkListCandidate.classList.remove('visible');
    if (checkListTime.classList.contains('visible'))
      checkListTime.classList.remove('visible');
    // -------------- Turn off others end --------------
}
// -------------- 3 end --------------

// -------------- 4 start --------------
var checkListTime = document.getElementById('js-schedule-list-time');
checkListTime.getElementsByClassName('schedule-anchor-span-time')[0].onclick = function(evt) {
  if (checkListTime.classList.contains('visible'))
    checkListTime.classList.remove('visible');
  else
    checkListTime.classList.add('visible');
    // -------------- Turn off others start --------------
    if (checkListAssessment.classList.contains('visible'))
      checkListAssessment.classList.remove('visible');
    if (checkListCandidate.classList.contains('visible'))
      checkListCandidate.classList.remove('visible');
    if (checkListDate.classList.contains('visible'))
      checkListDate.classList.remove('visible');
    // -------------- Turn off others end --------------
}
// -------------- 4 end --------------