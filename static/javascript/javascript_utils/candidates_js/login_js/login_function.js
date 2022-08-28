function Login() {
  // ------------------------------ example #1 start ------------------------------
  //  Assign variables to array, then push that array to localStorage using json stringify
  // https://javascript.plainenglish.io/implementing-login-case-using-localstorage-and-sessionstorage-bfddce5d2198 
  var a = new Array();
  up1 = new Object();
  up2 = new Object();

  up1={
    name:'abcd@gmail.com',
    password:btoa('abc@12')
  };  
  up2={
    name:'bcd@gmail.com',
    password:btoa('bcd@12')
  };
  
  a.push(up1);
  a.push(up2);
  
  localStorage.setItem('all_users',JSON.stringify(a));
  // ------------------------------ example #1 end ------------------------------


  // ------------------------------ attempt #2 start ------------------------------
  var username = document.getElementById('uname').value;
  var password = document.getElementById('psw').value;
  sessionStorage.setItem('currentloggedin',username);
  // ------------------------------ attempt #2 end ------------------------------


  a=JSON.parse((localStorage.getItem("all_users")));
  a.push({name: username, password: password});
  localStorage.setItem('name',JSON.stringify(a));
  for(var i=0; i<a.length; i++) {
    var li = document.createElement("li");
    li.innerHTML=a[i]['name'];
    document.getElementById("listuser").appendChild(li);
  }
}
