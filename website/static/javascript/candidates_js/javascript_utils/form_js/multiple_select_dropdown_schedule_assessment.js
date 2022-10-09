var checkListAssessment = document.getElementById('js-schedule-list-assessment-names');
checkListAssessment.getElementsByClassName('schedule-anchor-span-assessment-names')[0].onclick = function(evt) {
  if (checkListAssessment.classList.contains('visible'))
    checkListAssessment.classList.remove('visible');
  else
    checkListAssessment.classList.add('visible');
    // -------------- Turn off others start --------------
    if (checkListCandidate.classList.contains('visible'))
      checkListCandidate.classList.remove('visible');
    // -------------- Turn off others end --------------
}


var checkListCandidate = document.getElementById('js-schedule-list-candidate-names');
checkListCandidate.getElementsByClassName('schedule-anchor-span-candidate-names')[0].onclick = function(evt) {
  if (checkListCandidate.classList.contains('visible'))
    checkListCandidate.classList.remove('visible');
  else
    checkListCandidate.classList.add('visible');
    // -------------- Turn off others start --------------
    if (checkListAssessment.classList.contains('visible'))
      checkListAssessment.classList.remove('visible');
    // -------------- Turn off others end --------------
}