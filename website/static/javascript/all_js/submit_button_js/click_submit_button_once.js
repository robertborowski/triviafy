var wasSubmitted = false;    
function clickSubmitButtonOnce(){
  if(!wasSubmitted) {
    wasSubmitted = true;
    return wasSubmitted;
  }
  return false;
}

// function search() {
//   var testList = $('.eachTestItem');

// }