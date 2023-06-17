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