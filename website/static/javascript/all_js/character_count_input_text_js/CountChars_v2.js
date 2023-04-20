function CountCharsBirthdayAnswer(obj){
  var maxLength = 100;
  var strLength = obj.value.length;
  
  if(strLength > maxLength){
    document.getElementById("id-countCharsBirthdayAnswer").innerHTML = '<span style="color: red;">'+strLength+' out of '+maxLength+' characters</span>';
  }else{
    document.getElementById("id-countCharsBirthdayAnswer").innerHTML = '<span style="color:white;opacity:75%;">'+strLength+' out of '+maxLength+' characters';
  }
}