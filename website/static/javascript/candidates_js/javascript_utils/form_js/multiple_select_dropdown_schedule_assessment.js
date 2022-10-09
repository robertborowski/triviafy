var checkList = document.getElementById('js-schedule-list-assessment-names');
checkList.getElementsByClassName('schedule-anchor-span-assessment-names')[0].onclick = function(evt) {
  if (checkList.classList.contains('visible'))
    checkList.classList.remove('visible');
  else
    checkList.classList.add('visible');
}