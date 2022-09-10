function countCharsTitle(obj){var maxLength = 20;
  var strLength = obj.value.length;
  
  if(strLength > maxLength){
    document.getElementById("charNumTitle").innerHTML = '<span style="color: red;">'+strLength+' out of '+maxLength+' characters</span>';
  }else{
    document.getElementById("charNumTitle").innerHTML = '<span style="color: var(--company-greyed-out-color);">'+strLength+' out of '+maxLength+' characters';
  }
}