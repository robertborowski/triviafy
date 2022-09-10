// -------------------------------- Create Question Start --------------------------------
function countCharsAnswers(obj){
  var maxLength = 100;
  var strLength = obj.value.length;
  
  // -------------------------------- Create Question Start --------------------------------
  if(strLength > maxLength){
    document.getElementById("charNumAnswers").innerHTML = '<span style="color: red;">'+strLength+' out of '+maxLength+' characters</span>';
  }else{
    document.getElementById("charNumAnswers").innerHTML = '<span style="color: var(--company-greyed-out-color);">'+strLength+' out of '+maxLength+' characters';
  }
  // -------------------------------- Create Question End --------------------------------

  
  // -------------------------------- Quiz Answer Start --------------------------------
  // if(strLength > maxLength){
  //   document.getElementById("charNumAnswers1").innerHTML = '<span style="color: red;">'+strLength+' out of '+maxLength+' characters</span>';
  // }else{
  //   document.getElementById("charNumAnswers1").innerHTML = '<span style="color: var(--company-greyed-out-color);">'+strLength+' out of '+maxLength+' characters';
  // }

  // if(strLength > maxLength){
  //   document.getElementById("charNumAnswers2").innerHTML = '<span style="color: red;">'+strLength+' out of '+maxLength+' characters</span>';
  // }else{
  //   document.getElementById("charNumAnswers2").innerHTML = '<span style="color: var(--company-greyed-out-color);">'+strLength+' out of '+maxLength+' characters';
  // }

  // if(strLength > maxLength){
  //   document.getElementById("charNumAnswers3").innerHTML = '<span style="color: red;">'+strLength+' out of '+maxLength+' characters</span>';
  // }else{
  //   document.getElementById("charNumAnswers3").innerHTML = '<span style="color: var(--company-greyed-out-color);">'+strLength+' out of '+maxLength+' characters';
  // }
  // -------------------------------- Quiz Answer End --------------------------------


}
// -------------------------------- Create Question End --------------------------------