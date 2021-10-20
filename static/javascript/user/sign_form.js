function checkPw() {
    var error =  document.getElementById('pw_text');
    var pw = document.getElementById("password").value;
    var pwPattern = /[a-zA-Z0-9~!@#$%^&*()_+|<>?:{}]{8,16}/;
    error.parentNode.style.color = 'red'; 
    if(pw === "") {
        error.innerHTML = "필수 정보입니다.";
        error.style.display = "block";
        return false;
    } else if(!pwPattern.test(pw)) {
        error.innerHTML = "8~16자 영문 대 소문자, 숫자, 특수문자를 사용하세요.";
        error.style.display = "block";
        return false;
    } else {
        error.style.display = "none";
    }
}

function comparePw() {
    var error =  document.getElementById('pw_check');
    var pw2 = document.getElementById("password_2").value;
    var pw1 = document.getElementById("password").value;
    error.parentNode.style.color = 'red'; 
    if(pw2 == pw1) {
        error.style.display = "none";
    } else if(pw2 != pw1) {
        error.innerHTML = "비밀번호가 일치하지 않습니다.";
        error.style.display = "block";
        return false;
    } 
    if(pw2.value === "") {
        error.innerHTML = "필수 정보입니다.";
        error.style.display = "block";
        return false;
    }
}

function checkPhoneNum() {
    var isPhoneNum = /([01]{2,})([01679]{1,})([0-9]{3,4})([0-9]{4})/;
    var error =  document.getElementById('phone_text');
    var mb = document.getElementById("phone").value;
    error.parentNode.style.color = 'red'; 
    if(mb == "") {
        error.innerHTML = "필수 정보입니다.";
        error.style.display = "block";
        return false;
    } else if(!isPhoneNum.test(mb)) {
        error.innerHTML = "형식에 맞지 않는 번호입니다.";
        error.style.display = "block";
        return false;
    } else {
        error.style.display = "none";
    }
}

function checkName() {
    var error = document.getElementById('name_text');
    var namePattern = /[a-zA-Z가-힣]/;
    var name = document.getElementById("name").value;
    error.parentNode.style.color = 'red'; 
    if(name == '') {
        error.innerHTML = "필수 정보입니다.";
        error.style.display = "block";
        return false;
    } else if(!namePattern.test(name) || name.indexOf(" ") > -1) {
        error.innerHTML = "한글과 영문 대 소문자를 사용하세요. (특수기호, 공백 사용 불가)";
        error.style.display = "block";
        return false;
    } else {
        error.style.display = "none";
    }
}

function isEmailCorrect() {
    var emailPattern = /[a-z0-9]{2,}@[a-z0-9-]{2,}\.[a-z0-9]{2,}/;
    var error =  document.getElementById('email_text');
    var email = document.getElementById("email").value;
    error.parentNode.style.color = 'red'; 
    if(email == ""){ 
        error.innerHTML = "이메일을 입력하세요";
        error.style.display = "block"; 
        return false;
    } 
    else {
        error.style.display = "none"; 
    }

}

function isEmailCheck() {
    var check = document.getElementById('btn-email');
    var error = document.getElementById('btn_check');
    error.parentNode.style.color = 'red'; 
    if (check.style.display != 'none'){
        error.innerHTML = '중복확인을하세요';
        error.style.display = "block";
        return false;
    }
    else{
        error.style.display = 'none';
    }
    
}

function concate(){

    if (isEmailCorrect() == false){
        return false;
    }
    if (isEmailCheck() == false){
        return false;
    }
    if (checkPw() == false){
        return false;
    }
    if (comparePw() == false){
        return false;
    }
    if (checkName() == false){
        return false;
    }

    var asdfasf = document.getElementById('birth').value;
    
    if (asdfasf == ''){
        $('#birth_text').show();
        return false;
    }
    else{
        $('#birth_text').hide();
    }
    if (checkPhoneNum() == false){
        return false;
    }
}

function checkEmail(){
    
    var emailPattern = /[a-z0-9]{2,}@[a-z0-9-]{2,}\.[a-z0-9]{2,}/;
    var error =  document.getElementById('email_text');
    var email = document.getElementById("email").value;

    var error_r = document.getElementById('btn_check');
    error_r.style.display = 'none';

    if(email == ""){ 
        error.innerHTML = "이메일을 입력하세요";
        error.style.display = "block"; 
        return false;
    } else if(!emailPattern.test(email)) {
        error.innerHTML = "잘못된 양식입니다";
        error.style.display = "block";
        return false;
    } else {
        error.style.display = "none"; 
    }

        var tmp = $('#email').val()
		$.ajax({
			url:'/sign_check?email='+tmp,
			type:'get',
			dataType:'json',
			success:function(response){
				
				if(response.data == 'exist'){
					alert("존재하는 이메일 입니다!");
					$('#email').val('').focus();
					return;
				}else{
                    alert("가입가능!");
					$('#btn-email').hide();
                    $("#email").attr("readonly",true);
					return;
				}
			},
            error : function(xhr, error){
				alert("서버와의 통신에서 문제가 발생했습니다.");
				console.error("error : " + error);
			}
		})
	}

    $( document ).ready( function() {
        $(".navi").hide();
    });