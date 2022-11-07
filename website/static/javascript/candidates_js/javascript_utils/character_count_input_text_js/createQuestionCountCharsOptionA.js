function createQuestionCountCharsOptionA(obj){
  var maxLength = 280;
  var strLength = obj.value.length;
  
  if(strLength > maxLength){
    document.getElementById("createQuestionCountCharsOptionA").innerHTML = '<span style="color: red;">'+strLength+' out of '+maxLength+' characters</span>';
  }else{
    document.getElementById("createQuestionCountCharsOptionA").innerHTML = '<span style="color: var(--company-greyed-out-color);">'+strLength+' out of '+maxLength+' characters';
  }
}