$(document).ready(function() {
  $("#id-flow_continue_1").click(function() {
    // part 1
    $("#id-form_part_1").removeClass("uiSearchItemVisible2");
    $("#id-form_part_1").addClass("uiSearchItemInvisible");
    // part 2
    $("#id-form_part_2").removeClass("uiSearchItemInvisible");
    $("#id-form_part_2").addClass("uiSearchItemVisible2");
    // flow div
    $(this).removeClass("uiSearchItemVisible2");
    $(this).addClass("uiSearchItemInvisible");
    // submit div
    $("#id-flow_submit_1").removeClass("uiSearchItemInvisible");
    $("#id-flow_submit_1").addClass("uiSearchItemVisible2");
  });
});