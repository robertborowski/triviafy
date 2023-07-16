// ------------------------ start ------------------------
$(document).ready(function() {
  // ------------------------ default start ------------------------
  $("#id-show_result_0").removeClass("custom-invisible-1");
  $("#id-show_result_0").addClass("custom-visible-1");
  $("#id-flexRadioShowSelection_0").prop("checked", true);
  // ------------------------ default end ------------------------
  // ------------------------ click through selection start ------------------------
  $("#id-show_index_back_0").click(function() {
    try {
      $("#id-show_result_1").removeClass("custom-visible-1");
      $("#id-show_result_1").addClass("custom-invisible-1");
      $("#id-flexRadioShowSelection_1").prop("checked", false);
    } catch (error) {
      // pass
    }
    $("#id-show_result_0").removeClass("custom-invisible-1");
    $("#id-show_result_0").addClass("custom-visible-1");
    $("#id-flexRadioShowSelection_0").prop("checked", true);
  });
  $("#id-show_index_forward_1").click(function() {
    try {
      console.log('hello')
      $("#id-show_result_0").removeClass("custom-visible-1");
      $("#id-show_result_0").addClass("custom-invisible-1");
      $("#id-flexRadioShowSelection_0").prop("checked", false);
    } catch (error) {
      // pass
    }
    $("#id-show_result_1").removeClass("custom-invisible-1");
    $("#id-show_result_1").addClass("custom-visible-1");
    $("#id-flexRadioShowSelection_1").prop("checked", true);
  });
  $("#id-show_index_back_1").click(function() {
    try {
      console.log('hello')
      $("#id-show_result_2").removeClass("custom-visible-1");
      $("#id-show_result_2").addClass("custom-invisible-1");
      $("#id-flexRadioShowSelection_2").prop("checked", false);
    } catch (error) {
      // pass
    }
    $("#id-show_result_1").removeClass("custom-invisible-1");
    $("#id-show_result_1").addClass("custom-visible-1");
    $("#id-flexRadioShowSelection_1").prop("checked", true);
  });
  $("#id-show_index_forward_2").click(function() {
    try {
      console.log('hello')
      $("#id-show_result_1").removeClass("custom-visible-1");
      $("#id-show_result_1").addClass("custom-invisible-1");
      $("#id-flexRadioShowSelection_1").prop("checked", false);
    } catch (error) {
      // pass
    }
    $("#id-show_result_2").removeClass("custom-invisible-1");
    $("#id-show_result_2").addClass("custom-visible-1");
    $("#id-flexRadioShowSelection_2").prop("checked", true);
  });
  $("#id-show_index_back_2").click(function() {
    try {
      console.log('hello')
      $("#id-show_result_3").removeClass("custom-visible-1");
      $("#id-show_result_3").addClass("custom-invisible-1");
      $("#id-flexRadioShowSelection_3").prop("checked", false);
    } catch (error) {
      // pass
    }
    $("#id-show_result_2").removeClass("custom-invisible-1");
    $("#id-show_result_2").addClass("custom-visible-1");
    $("#id-flexRadioShowSelection_2").prop("checked", true);
  });
  $("#id-show_index_forward_3").click(function() {
    try {
      console.log('hello')
      $("#id-show_result_2").removeClass("custom-visible-1");
      $("#id-show_result_2").addClass("custom-invisible-1");
      $("#id-flexRadioShowSelection_2").prop("checked", false);
    } catch (error) {
      // pass
    }
    $("#id-show_result_3").removeClass("custom-invisible-1");
    $("#id-show_result_3").addClass("custom-visible-1");
    $("#id-flexRadioShowSelection_3").prop("checked", true);
  });
  $("#id-show_index_back_3").click(function() {
    try {
      console.log('hello')
      $("#id-show_result_4").removeClass("custom-visible-1");
      $("#id-show_result_4").addClass("custom-invisible-1");
      $("#id-flexRadioShowSelection_4").prop("checked", false);
    } catch (error) {
      // pass
    }
    $("#id-show_result_3").removeClass("custom-invisible-1");
    $("#id-show_result_3").addClass("custom-visible-1");
    $("#id-flexRadioShowSelection_3").prop("checked", true);
  });
  $("#id-show_index_forward_4").click(function() {
    try {
      console.log('hello')
      $("#id-show_result_3").removeClass("custom-visible-1");
      $("#id-show_result_3").addClass("custom-invisible-1");
      $("#id-flexRadioShowSelection_3").prop("checked", false);
    } catch (error) {
      // pass
    }
    $("#id-show_result_4").removeClass("custom-invisible-1");
    $("#id-show_result_4").addClass("custom-visible-1");
    $("#id-flexRadioShowSelection_4").prop("checked", true);
  });
  $("#id-show_index_back_4").click(function() {
    try {
      console.log('hello')
      $("#id-show_result_5").removeClass("custom-visible-1");
      $("#id-show_result_5").addClass("custom-invisible-1");
      $("#id-flexRadioShowSelection_5").prop("checked", false);
    } catch (error) {
      // pass
    }
    $("#id-show_result_4").removeClass("custom-invisible-1");
    $("#id-show_result_4").addClass("custom-visible-1");
    $("#id-flexRadioShowSelection_4").prop("checked", true);
  });
  // ------------------------ click through selection end ------------------------
});
// ------------------------ end ------------------------