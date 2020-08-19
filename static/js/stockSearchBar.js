

// form validtion:
function stockValidaiton(){
    return isAllLetters("search-input");


}


$(".input-text").keypress(function() {
  $(this).removeClass("error");
});



function addError(classToAddError){
	var element = ($("." + classToAddError));
	element.addClass("error");
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