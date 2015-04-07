var email;
var username;
var testclicking;

var validateField = function(fieldElem, infoMessage, validateFn) {
	//The span message that will be inserted.    
    var spanMsg = "<span>" + infoMessage + "</span>";
    //alert(fieldElem.next().is("input"));
    //The span is only inserted if it hasn't been before.
    if (fieldElem.next().is("input") || fieldElem.next().is("button")) {
        fieldElem.after(spanMsg);
        fieldElem.next().addClass("info");
    }
    /*
        Hides the span if: 1) It was just created, or
        2) There's nothing in it.
    */
    if (fieldElem.val() === undefined || fieldElem.val().length === 0) {
        fieldElem.next().hide();
    } 
        
    /*
        Once the user starts to edit the field,
        I show the info span. To handle the case
        where the user is returning to edit after
        an error or even a correct entry, I remove
        classes to return to the default info class.
    */
    fieldElem.on('input', function () {
        fieldElem.next().removeClass();
        fieldElem.next().text(infoMessage);
        fieldElem.next().addClass("info");        
        fieldElem.next().show();
        if (this.value.length > 0) {
            fieldElem.next().show();   
        }
    });
    
    /*
        Adjusts the span based on whether input
        was correct or not. Here is where I 
        actually call the validate function. Just
        as when editing, I remove all classes before
        inserting the new class, as a precaution.
    */
    fieldElem.focusout(function() {  
        if (validateFn(fieldElem.val()) === true) {
            fieldElem.css({
	           background: "#cfc"	
                });
            fieldElem.next().hide();
            fieldElem.next().text("OK");
            fieldElem.next().removeClass();
            fieldElem.next().addClass("ok");
        } else {
            fieldElem.css({
	           background: "#fcc"	
                });
            fieldElem.addClass("error");
            fieldElem.next().text("Error: " + infoMessage );
            fieldElem.next().removeClass();
            fieldElem.next().addClass("error");
            fieldElem.next().show();
        }
        /*
            Handles the special case where there's nothing
            in the box, where the info span should
            be hidden.
        */
        if (fieldElem.val() === undefined || fieldElem.val().length === 0) {
            fieldElem.next().hide();
        }
    });    
};

/*
    Validates the username. Validates only alphanumeric
    characters. Due to the way the regex workds, '_' is
    allowed, but I decided that this is in line with what
    constitutes a valid username anywhere I've seen.
*/
var validateRealName= function (text) {    
    var re = /^[\w\- ]+$/;
    return re.test(text);
    //Username should only be alphabetical or numeric
    //password should be @least 8 chars long
    //email address should contain a @ character
};

var validateUsername = function (text) {    
    var re = /^\w+$/;
    return re.test(text);
    //Username should only be alphabetical or numeric
    //password should be @least 8 chars long
    //email address should contain a @ character
};

/*
  Per assignment instructions, checks for an "@" sign
*/
var validateEmail = function(text) {    
    var re = /@/;
    return re.test(text);
};

/*
    Tests on the length of the password string.    
*/
var validatePassword = function(passwordString) {
    
    return (passwordString.length >= 8);
    
};


$(document).ready(function () {    
    
    $("#newPassword").focus(function () {
        validateField($(this), "Must be 8 characters or more", 
                      validatePassword);
    });
    
    $("#newUser").focus(function () {
        validateField($(this), "Alphanumeric characters only", 
                      validateUsername);
    });
    
    $("#newName").focus(function () {
        validateField($(this), "Alphanumeric characters, spaces, hyphens only", 
                      validateRealName);
    });
    
     $("#newEmail").focus(function () {
        validateField($(this), "Must contain an @ character", 
                      validateEmail);
    });    
});
