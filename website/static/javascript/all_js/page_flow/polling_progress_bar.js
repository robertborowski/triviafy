$(document).ready(function() {
  // ----------------------------- multiple progress bars start -----------------------------
  try {
    var all_ids_like_arr = $('[id^="id-progress_bar_"]');
    for (var i = 0; i < all_ids_like_arr.length; i++) {
      var desired_id_name = all_ids_like_arr[i].id;
      console.log(desired_id_name)
      console.log(' ===================== ')
      // var desired_id_name = all_ids_like_arr[0].id;
      var element = $('#'+desired_id_name);
      if (!isNaN(parseInt(desired_id_name.substr(-3)))) {
        var newWidth = parseInt(desired_id_name.substr(-3))
        element.css('width', newWidth+'%');
        element.addClass('bg-success')
        element.removeClass('bg-secondary')
      } else {
        if (!isNaN(parseInt(desired_id_name.substr(-2)))) {
          var newWidth = parseInt(desired_id_name.substr(-2))
          element.css('width', newWidth+'%');
        } else {
          if (!isNaN(parseInt(desired_id_name.substr(-1)))) {
            var newWidth = parseInt(desired_id_name.substr(-1))
            element.css('width', newWidth+'%');
          } else {
          }
        }
      }
    }
  } catch (error) {
    return;
  }
  // ----------------------------- multiple progress bars start -----------------------------
});

$(document).ready(function() {
    // ----------------------------- progress bar start -----------------------------
    try {
      var all_ids_like_arr = $('[id^="id-progress_bar_catch"]');
      var desired_id_name = all_ids_like_arr[0].id;
      var element = $('#'+desired_id_name);
      if (!isNaN(parseInt(desired_id_name.substr(-3)))) {
        var newWidth = parseInt(desired_id_name.substr(-3))
        element.css('width', newWidth+'%');
        return;
      } else {
        if (!isNaN(parseInt(desired_id_name.substr(-2)))) {
          var newWidth = parseInt(desired_id_name.substr(-2))
          element.css('width', newWidth+'%');
          return;
        } else {
          if (!isNaN(parseInt(desired_id_name.substr(-1)))) {
            var newWidth = parseInt(desired_id_name.substr(-1))
            element.css('width', newWidth+'%');
            return;
          } else {
            return;
          }
        }
      }
    } catch (error) {
      return;
    }
    // ----------------------------- progress bar end -----------------------------
  });