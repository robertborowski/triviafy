function countCharsCategory(obj){
  var maxLength = 100;
  var strLength = obj.value.length;
  
  if(strLength > maxLength){
    document.getElementById("charNumCategory").innerHTML = '<span style="color: red;">'+strLength+' out of '+maxLength+' characters</span>';
  }else{
    document.getElementById("charNumCategory").innerHTML = '<span style="color: var(--company-greyed-out-color);">'+strLength+' out of '+maxLength+' characters';
  }
}