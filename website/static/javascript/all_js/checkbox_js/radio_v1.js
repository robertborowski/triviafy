// ------------------------ start ------------------------
document.addEventListener('click', function() {
  // Submit buttons - define
  var submitButtonTop = document.getElementById('submit-button-top');
  var submitButtonBottom = document.getElementById('submit-button-botttom');
  // loop through all id's on the page
  var element_all_ids = document.querySelectorAll('[id]');
  for (var i = 0; i < element_all_ids.length; i++) {
    // get the name of each element and see if name contains substring
    var i_element_id = document.getElementById(element_all_ids[i].id);
    if (i_element_id.id.indexOf('uiFeedbackSelection') !== -1) {
      // get label associated with id
      var i_label = document.querySelector('label[for="'+i_element_id.id+'"]');
      // if/else checked add + remove classes
      if (i_element_id.checked) {
        i_label.classList.add('custom-bg-white');
        i_label.classList.remove('custom-color-white');
        i_label.classList.add('custom-color-primary');
        i_label.classList.add('custom-trigger-next-1');
        // Submit buttons - appear
        submitButtonTop.classList.remove('uiSearchItemInvisible');
        submitButtonTop.classList.add('uiSearchItemVisible');
        submitButtonBottom.classList.remove('uiSearchItemInvisible');
        submitButtonBottom.classList.add('uiSearchItemVisible');
      } else {
        i_label.classList.remove('custom-bg-white');
        i_label.classList.add('custom-color-white');
        i_label.classList.remove('custom-color-primary');
        i_label.classList.remove('custom-trigger-next-1');
      }
    }
  }
});
// ------------------------ end ------------------------