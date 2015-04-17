var $;
function sendReq(url, callbackFunction) {   
    var xmlhttp, ActiveXObject;
    if (window.XMLHttpRequest) {
        // code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp = new XMLHttpRequest();
    } else {
        // code for IE6, IE5
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }

    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
            if (callbackFunction) { callbackFunction(xmlhttp.responseText); }
        }
    };

    xmlhttp.open("POST", url, true);
    xmlhttp.send();
    return xmlhttp.responseText;
}

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
    if(text){
        empty = 1;
    }
    return re.test(text);
    //Username should only be alphabetical or numeric
    //password should be @least 8 chars long
    //email address should contain a @ character
};

var validateUsername = function (text) {    
    var re = /^\w+$/;
    if(text){
        empty = 1;
    }
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
    if(text){
        empty = 1;
    }
    return re.test(text);
};

/*
    Tests on the length of the password string.    
*/
var validatePassword = function(passwordString) {
    if(passwordString){
        empty = 1;
    }
    return (passwordString.length == 0 || passwordString.length >= 8);
    
};

function validate() {    
    // Request to python
    sendReq("/cgi-bin/testCookies.py", function processResponse(response) { 
        
        if (response == 0) {//The needed cookie was found; alters navbar
            document.getElementById("navbar").innerHTML = "<ul class='nav navbar-nav'>" + 
                "<li><a href='itementry.html'><i class='fa fa-shield'></i> Admin</a></li>" + 
                "<li><a href='customerinfo.html'><i class='fa fa-user'></i> Account</a></li>" +     
                "<li><a href='cart.html'><i class='fa fa-shopping-cart'></i> Cart</a></li>" + 
                "<li><a href='checkout.html'><i class='fa fa-crosshairs'></i> Checkout</a></li>" + 
                "<li><a href='#' class='active'><i class='fa fa-lock'></i> Logout</a></li></ul>";
            
            // change to home screen on successful login attempt
            // window.location = 'index.html';
        } else if (response == 1) { //The needed cookie wasn't found
            document.getElementById("navbar").innerHTML = "<ul class='nav navbar-nav'>" + 
                "<li><a href='customerinfo.html'><i class='fa fa-user'></i> Account</a></li>" + 
                "<li><a href='cart.html'><i class='fa fa-shopping-cart'></i> Cart</a></li>" + 
                "<li><a href='checkout.html'><i class='fa fa-crosshairs'></i> Checkout</a></li>" + 
                "<li><a href='#' class='active'><i class='fa fa-lock'></i> Logout</a></li></ul>";
        }
    });
}
/*For the customerinfo.html page. The script returns html to load the custinfo section*/
function loadCustomerInfo() {    
    sendReq("/cgi-bin/loadCustomer.py", function processResponse(response) {
       $("#custinfo").append(response); 
        if ($("#updateUserSubmit").length) {       
        $("#updateUserSubmit").click(function() {
           submitCustomerInfo();    
        });
        $("#addAddressSubmit").click(function() {
           window.location.href = 'addAddress.html';    
        });
        $("#newpassword").focus(function () {
        validateField($(this), "Must be 8 characters or more", 
                      validatePassword);
        });            
        $("#name").focus(function () {
            validateField($(this), "Alphanumeric characters, spaces, hyphens only", 
                          validateRealName);
        });
         $("#email").focus(function () {
            validateField($(this), "Must contain an @ character", 
                          validateEmail);
        });
    }
        
    });
}
function submitCustomerInfo() {  
    data = $("#customerform").serialize();
    
    sendReq("/cgi-bin/updateCustomer.py?" + data, function processResponse(response) {
       $("#custinfo").append(response); 
       if (response == -1) {
           $("#custinfo").append("<p>Sorry, wrong password.</p>");
       } else {          
          $("#custinfo").empty();           
          loadCustomerInfo();
           $("#custinfo").append("<p>Sucess! Information updated.</p>");          
       }
        
    });
}

/*For the customerinfo.html page. The script returns html to load the custinfo section*/
function loadBookInfo(isbn) {     
    $("#bookinfo").empty();
    sendReq("/cgi-bin/loadbookforedit.py?isbn=" + isbn, function processResponse(response) {
        if (response == -1) {
            $("#bookinfo").empty();
           $("#bookinfo").append("<p>Sorry, item not found.</p>");
       } else {          
            $("#bookinfo").append(response); 
            if ($("#updateBookSubmit").length) {       
                $("#updateBookSubmit").click(function() {            
                   submitBookInfo();    
            });
            }
            if ($("#deleteBookSubmit").length) {
                $("#deleteBookSubmit").click(function() {
                    deleteBookInfo();   
                });
            }     
       }
       
/*        $("#newpassword").focus(function () {
        validateField($(this), "Must be 8 characters or more", 
                      validatePassword);
        });            
        $("#name").focus(function () {
            validateField($(this), "Alphanumeric characters, spaces, hyphens only", 
                          validateRealName);
        });
         $("#email").focus(function () {
            validateField($(this), "Must contain an @ character", 
                          validateEmail);
        });*/
            
    });
}
function submitBookInfo() {  

   data = $("#booksubmit").serialize();
    
    sendReq("/cgi-bin/updatebook.py?" + data + "&mode=update", function processResponse(response) {
       $("#bookinfo").append(response); 
       if (response == -1) {
           $("#bookinfo").append("<p>Sorry, wrong password.</p>");
       } else {          
          $("#bookinfo").empty();           
          loadBookInfo();
           $("#bookinfo").append("<p>Sucess! Information updated.</p>");          
       }        
    });
}
function deleteBookInfo() {  
   data = $("#booksubmit").serialize();
    
    sendReq("/cgi-bin/updatebook.py?" + data, function processResponse(response) {
       $("#bookinfo").append(response); 
       if (response == -1) {
           $("#bookinfo").append("<p>Sorry, wrong password.</p>");
       } else {          
          $("#bookinfo").empty();           
          
           $("#bookinfo").append("<p>Sucess! Book deleted.</p>");          
       }        
    });
}

function loadOrderInfo() {    
    sendReq("/cgi-bin/latestorder.py", function processResponse(response) {
        alert("Response!");
       $("#orderinfo").append("<p>Thank you! Order #" + response + " has been completed! Expect any physical books to be delivered within 3 to 5 business days.</p>");        
        $("#orderinfo").append("<p>Please refer to this order number if you contact us with any issues.</p>");
         $("#orderinfo").append('<a class="btn btn-default cart" href="history.html">Order History</a>');
        $("#orderinfo").append('<a class="btn btn-default cart" href="shop.html">Continue Shopping</a>');
    });
}
window.onload = function () {
    
    if ($("#custinfo").length) {
        loadCustomerInfo();
    }
    if ($("#bookinfo").length) {
        //loadBookInfo();
        $("#goedit").click(function() {            
            loadBookInfo($("#editsearch").val());   
        });
    }
    if ($("#orderinfo").length) {        
        loadOrderInfo();
    }
    //Validates the user's cookies
    validate();
};
