function createQuestionCountCharsQuestion(obj){
  var maxLength = 750;
  var strLength = obj.value.length;
  
  if(strLength > maxLength){
    document.getElementById("createQuestionCountCharsQuestion").innerHTML = '<span style="color: red;">'+strLength+' out of '+maxLength+' characters</span>';
  }else{
    document.getElementById("createQuestionCountCharsQuestion").innerHTML = '<span style="color: custom-color-light-1;">'+strLength+' out of '+maxLength+' characters';
  }
}