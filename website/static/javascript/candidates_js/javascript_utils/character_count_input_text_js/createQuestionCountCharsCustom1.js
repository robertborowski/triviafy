function createQuestionCountCharsCustom1(obj){
  var maxLength = 100;
  var strLength = obj.value.length;
  
  if(strLength > maxLength){
    document.getElementById("createQuestionCountCharsCustom1").innerHTML = '<span style="color: red;">'+strLength+' out of '+maxLength+' characters</span>';
  }else{
    document.getElementById("createQuestionCountCharsCustom1").innerHTML = '<span style="color: custom-color-light-1;">'+strLength+' out of '+maxLength+' characters';
  }
}