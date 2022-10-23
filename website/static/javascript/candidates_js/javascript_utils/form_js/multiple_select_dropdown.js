var checkList = document.getElementById('create-assessment-choose-lang-list1');
checkList.getElementsByClassName('create-assessment-anchor-span')[0].onclick = function(evt) {
  if (checkList.classList.contains('visible'))
    checkList.classList.remove('visible');
  else
    checkList.classList.add('visible');
}