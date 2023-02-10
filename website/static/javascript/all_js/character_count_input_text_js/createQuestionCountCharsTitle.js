function createQuestionCountCharsTitle(obj){
  var maxLength = 50;
  var strLength = obj.value.length;
  
  if(strLength > maxLength){
    document.getElementById("createQuestionCountCharsTitle").innerHTML = '<span style="color: red;">'+strLength+' out of '+maxLength+' characters</span>';
  }else{
    document.getElementById("createQuestionCountCharsTitle").innerHTML = '<span style="color: custom-color-light-1;">'+strLength+' out of '+maxLength+' characters';
  }
}