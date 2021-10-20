function checkPw() {
    var error =  document.getElementById('pw_text');
    var pw = document.getElementById("password").value;
    var pwPattern = /[a-zA-Z0-9~!@#$%^&*()_+|<>?:{}]{8,16}/;
    if(pw === "") {
        error.innerHTML ="비밀번호를 입력하세요.";
        error.style.display = "block";
        return false;
    } 
    else {
        error.style.display = "none";
    }
}

function isEmailCorrect() {
    var error =  document.getElementById('email_text');
    var email = document.getElementById("email").value;

    if(email == ""){ 
        error.innerHTML = "이메일을 입력하세요";
        error.style.display = "block"; 
        return false;
    } 
    else {
        error.style.display = "none"; 
    }

}
function concate(){

    if (isEmailCorrect() == false){
        return false;
    }
    if (checkPw() == false){
        return false;
    }
}

$( document ).ready( function() {

    $(".navi").hide();
});