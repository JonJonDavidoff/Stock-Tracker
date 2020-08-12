function setFocus(){
	$("#Email").focus();
}
window.onload = setFocus();


// form validtion:
function mainValidaiton(){
	var isEmail = isEmailValid("Email-input");
	var isPassword = isPasswordValid("Password-input");
	return isEmail && isPassword;
}


$(".input-text").keypress(function() {
  $(this).removeClass("error");
});



function addError(classToAddError){
	var element = ($("." + classToAddError));
	element.addClass("error");
}



function isEmailValid(EmailToCheck){
	if(/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test($("." + EmailToCheck).val())){
		return true;
	}else{

		addError(EmailToCheck);
		return false;
	}
}


function isPasswordValid(PasswordToCheck){
	var check = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,20}$/;
	if($("." + PasswordToCheck).val().match(check)){
		return true;
	}else{
		addError(PasswordToCheck)
		return false;
	}
}