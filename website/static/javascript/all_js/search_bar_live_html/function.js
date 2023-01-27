$("#uiSearch").keyup(function(){
  var currently_typed = $(this).val().toLowerCase();

  var testList = $('.uiSearchItem');
  testList.each(function() {
    var i_category = $(this).text().toLowerCase();
    // if (i_category == "aws")
    if (i_category.indexOf(currently_typed) >= 0) {
      //  block of code to be executed if the condition is true
      $( this ).removeClass("uiSearchItemInvisible");
      $( this ).addClass("uiSearchItemVisible");
    } else {
      //  block of code to be executed if the condition is false
      $( this ).removeClass("uiSearchItemVisible");
      $( this ).addClass("uiSearchItemInvisible");
    }
  });
});