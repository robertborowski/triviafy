// Get an array of all the classes with this name. In this case all questions on the quiz will have this class
var all_categories_id = document.getElementById("all_categories");
var selected_section = document.getElementsByClassName("category-section");

// Check the value of the class name element and if meets criteria then make the change to display
if(all_categories_id) {
  selected_section[1].style.display="none";
  all_categories_id.checked = false;
}