function CountCharsBirthdayAnswer(obj){
  var maxLength = 100;
  var strLength = obj.value.length;
  
  if(strLength > maxLength){
    document.getElementById("id-countCharsBirthdayAnswer").innerHTML = '<span style="color: red;">'+strLength+' out of '+maxLength+' characters. Please avoid using special characters in your response.</span>';
  }else{
    document.getElementById("id-countCharsBirthdayAnswer").innerHTML = '<span style="color:white;opacity:75%;">'+strLength+' out of '+maxLength+' characters. Please avoid using special characters in your response.';
  }
}

function CountCharsNameAnswer(obj){
  var maxLength = 20;
  var strLength = obj.value.length;
  
  if(strLength > maxLength){
    document.getElementById("id-countCharsNameAnswer").innerHTML = '<span style="color: red;">'+strLength+' out of '+maxLength+' characters. Please avoid using special characters in your response.</span>';
  }else{
    document.getElementById("id-countCharsNameAnswer").innerHTML = '<span style="color:white;opacity:75%;">'+strLength+' out of '+maxLength+' characters. Please avoid using special characters in your response.';
  }
}

function CountCharsCustomQuestion(obj){
  var maxLength = 150;
  var strLength = obj.value.length;
  
  if(strLength > maxLength){
    document.getElementById("id-countCharsCustomQuestion").innerHTML = '<span style="color: red;">'+strLength+' out of '+maxLength+' characters. Please avoid using special characters in your response.</span>';
  }else{
    document.getElementById("id-countCharsCustomQuestion").innerHTML = '<span style="color:white;opacity:75%;">'+strLength+' out of '+maxLength+' characters. Please avoid using special characters in your response.';
  }
}