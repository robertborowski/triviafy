function createQuestionCountCharsTitle(obj){
  var maxLength = 150;
  var strLength = obj.value.length;
  
  if(strLength > maxLength){
    document.getElementById("createQuestionCountCharsTitle").innerHTML = '<span style="color: red;">'+strLength+' out of '+maxLength+' characters</span>';
  }else{
    document.getElementById("createQuestionCountCharsTitle").innerHTML = '<span style="color: var(--company-greyed-out-color);">'+strLength+' out of '+maxLength+' characters';
  }
}