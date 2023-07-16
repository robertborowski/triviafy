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
        // Submit buttons - appear
        submitButtonTop.classList.remove('uiSearchItemInvisible');
        submitButtonTop.classList.add('uiSearchItemVisible');
        submitButtonBottom.classList.remove('uiSearchItemInvisible');
        submitButtonBottom.classList.add('uiSearchItemVisible');
      } else {
        i_label.classList.remove('custom-bg-white');
        i_label.classList.add('custom-color-white');
        i_label.classList.remove('custom-color-primary');
      }
    }
  }
});
// ------------------------ end ------------------------

// ------------------------ start ------------------------
document.addEventListener('click', function() {
  // loop through all id's on the page
  var element_all_ids = document.querySelectorAll('[id]');
  for (var i = 0; i < element_all_ids.length; i++) {
    // get the name of each element and see if name contains substring
    var i_element_id = document.getElementById(element_all_ids[i].id);
    if (i_element_id.id.indexOf('uiAnswerSelection') !== -1) {
      // get label associated with id
      var i_label = document.querySelector('label[for="'+i_element_id.id+'"]');
      // if/else checked add + remove classes
      if (i_element_id.checked) {
        i_label.classList.add('custom-bg-success');
        // i_label.classList.remove('custom-color-white');
        // i_label.classList.add('custom-color-black');
      } else {
        i_label.classList.remove('custom-bg-success');
        // i_label.classList.add('custom-color-white');
        // i_label.classList.remove('custom-color-black');
      }
    }
  }
});
// ------------------------ end ------------------------

// ------------------------ upvote downvote start ------------------------
document.addEventListener('click', function() {
  // ------------------------ loop start ------------------------
  // create array of up/down voting id's
  var idStringsArray = ['id-ui_vote_question_', 'id-ui_vote_feedback_'];
  // Loop through the array uniform for all up/down feedback
  for (var id_index = 0; id_index < idStringsArray.length; id_index++) { 
    // ------------------------ working start ------------------------
    // loop through all id's on the page
    var element_all_ids = document.querySelectorAll('[id]');
    for (var i = 0; i < element_all_ids.length; i++) {
      // get the name of each element and see if name contains substring
      var i_element_id = document.getElementById(element_all_ids[i].id);
      // ------------------------ radio vote button start ------------------------
      if (i_element_id.id.indexOf(idStringsArray[id_index]) !== -1) {
        // get label associated with id
        var i_label = document.querySelector('label[for="'+i_element_id.id+'"]');
        // if/else checked add + remove classes
        if (i_element_id.checked) {
          i_label.classList.remove('custom-opacity-50');
          // ------------------------ vote button up start ------------------------
          var substring = '_up';
          if (i_element_id.id.includes(substring)) {
            // The substring is present in the ID
            i_label.classList.add('custom-color-success-important');
          } else {
            // nothing
          }
          // ------------------------ vote button up end ------------------------
          // ------------------------ vote button up start ------------------------
          var substring = '_down';
          if (i_element_id.id.includes(substring)) {
            // The substring is present in the ID
            i_label.classList.add('custom-color-danger-important');
          } else {
            // nothing
          }
          // ------------------------ vote button up end ------------------------
        } else {
          i_label.classList.add('custom-opacity-50');
          i_label.classList.remove('custom-color-success-important');
          i_label.classList.remove('custom-color-danger-important');
        }
      }
      // ------------------------ radio vote button end ------------------------
    }
    // ------------------------ working end ------------------------
  }
  // ------------------------ loop end ------------------------
});
// ------------------------ upvote downvote end ------------------------