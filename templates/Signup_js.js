function setFocus(){
	$("#FirstName").focus();
}
window.onload = setFocus();


// form validtion:
function mainValidaiton(){
	var isFirstName = isAllLetters("FirstName-input");
	var isLastName = isAllLetters("LastName-input");
	var isEmail = isEmailValid("Email-input-signup");
	var isPassword = isPasswordValid("Password-input");
	return isFirstName && isLastName && isEmail && isPassword;
	
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


function isAllLetters(classToCheck){
	var letters = /^[A-Za-z]+$/;
	if($("." + classToCheck).val().match(letters)){
		return true;
	}else{
		addError(classToCheck);
		return false;
	}
}