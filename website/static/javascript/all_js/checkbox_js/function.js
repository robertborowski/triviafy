// ------------------------ start ------------------------
// ------------------------ default page load start ------------------------
if($('#flexSwitchCheckDefault_02').is(':checked')){
  $('#uiSelectAllBlock').removeClass("uiSelectAllBlockVisible");
  $('#uiSelectAllBlock').addClass("uiSelectAllBlockInvisible");
}
else {
  $('#uiSelectAllBlock').addClass("uiSelectAllBlockVisible");
  $('#uiSelectAllBlock').removeClass("uiSelectAllBlockInvisible");
};
// ------------------------ default page load end ------------------------
// ------------------------ on change start ------------------------
$('[name="flexSwitchCheckDefault_02"]').change(function(){
  if ($(this).is(':checked')) {
    $('#uiSelectAllBlock').removeClass("uiSelectAllBlockVisible");
    $('#uiSelectAllBlock').addClass("uiSelectAllBlockInvisible");
  }
  else {
    $('#uiSelectAllBlock').addClass("uiSelectAllBlockVisible");
    $('#uiSelectAllBlock').removeClass("uiSelectAllBlockInvisible");
  };
});
// ------------------------ on change end ------------------------
// ------------------------ end ------------------------