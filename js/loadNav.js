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
/*Validates the user cookies and allows links to login and other user-specific links*/
function validate() {    
    // Request to python
    sendReq("/cgi-bin/testCookies.py", function processResponse(response) { 
        
        if (response == 0) {//The needed cookie was found; alters navbar
            document.getElementById("navbar").innerHTML = "<ul class='nav navbar-nav'>" + 
                "<li><a href='itementry.html'><i class='fa fa-shield'></i> Admin</a></li>" + 
                "<li><a href='customerinfo.html'><i class='fa fa-user'></i> Account</a></li>" +     
                "<li><a href='cart.html'><i class='fa fa-shopping-cart'></i> Cart</a></li>" + 
                "<li><a href='checkout.html'><i class='fa fa-crosshairs'></i> Checkout</a></li>" + 
                "<li><a href='#' id='logout' class='active'><i class='fa fa-lock'></i> Logout</a></li></ul>";
            
            // change to home screen on successful login attempt
            // window.location = 'index.html';
        } else if (response == 1) { //The needed cookie wasn't found
            document.getElementById("navbar").innerHTML = "<ul class='nav navbar-nav'>" + 
                "<li><a href='customerinfo.html'><i class='fa fa-user'></i> Account</a></li>" + 
                "<li><a href='cart.html'><i class='fa fa-shopping-cart'></i> Cart</a></li>" + 
                "<li><a href='checkout.html'><i class='fa fa-crosshairs'></i> Checkout</a></li>" + 
                "<li><a href='#' id='logout' class='active'><i class='fa fa-lock'></i> Logout</a></li></ul>";
        }
        $("#logout").click(function() {
               logout();
        });
    });
}
/*Calls the remove cookies function, then redirects to the homepage*/          
function logout() {
     sendReq("/cgi-bin/removecookies.py?", function processResponse(response) {
         window.location.href = 'index.html';
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
           window.location.href = 'addresses.html';    
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
/*Updates a customer's details on the account page*/
function submitCustomerInfo() {  
    data = $("#customerform").serialize();
    
    sendReq("/cgi-bin/updateCustomer.py?" + data, function processResponse(response) {
       //$("#custinfo").append(response); 
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
        if (response == 0) {
            $("#bookinfo").empty();
           $("#bookinfo").append("<p>Sorry, item not found.</p>");
       } else {          
            $("#bookinfo").append(response);
           $(".expanderbutton").click(function () {        
                addBox($(this));  
            });
            oldisbn = $("#isbn").val();            
            if ($("#updateBookSubmit").length) {       
                $("#updateBookSubmit").click(function() {            
                   submitBookInfo(oldisbn);    
            });
            }
            if ($("#deleteBookSubmit").length) {
                $("#deleteBookSubmit").click(function() {
                    deleteBookInfo(oldisbn);   
                });
            }     
       }
       
            
    });
}
/*Validates an edited book and submits the new data if the validation checks out*/
function submitBookInfo(oldisbn) {  

   data = $("#booksubmit").serialize();        
    var isbn = $("#isbn").val(), 
        title = $("#newtitle").val(), 
        publisher = $("#newpublisher").val(), 
        price = $("#newprice").val(), 
        pages = $("#newpages").val(), 
        description = $("#newdesc").val(), 
        image = $("#newimage").val(), 
        authors = document.getElementsByName('author[]'), 
        formats = document.getElementsByName('format[]'), 
        genres = document.getElementsByName('genre[]'),
        inStock = $("#instock").val();
    var error = 0;      
    if (isbn == '' || isbn.length != 13 || isNaN(isbn)){
        $("#booksubmit").append("ISBN error, must be 13-digits!");
        error = 1;
    }
    else if (title == ''){
        $("#booksubmit").append("Title blank!");
        error = 1;
    }
    else if (publisher == ''){
        $("#booksubmit").append("Publisher blank!");
        error = 1;
    }
    else if (price == '' || isNaN(price)){
        $("#booksubmit").append("Price error!");
        error = 1;
    }
    else if (pages == '' || isNaN(pages)){
        $("#booksubmit").append("Pages error!");
        error = 1;
    }
    else if (description == ''){
        $("#booksubmit").append("Description blank!");
        error = 1;
    }
    else if (image == ''){
        $("#booksubmit").append("Provide Image file path!");
        error = 1;
    }
    else if (authors[0].value == ''){
        $("#booksubmit").append("Author blank!");
        error = 1;
    }
    else if (genres[0].value == ''){
        document.getElementById("newItemForm").innerHTML ="Genre blank!";
        error = 1;
    }
    else if (inStock == '' || isNaN(inStock)){
        document.getElementById("newItemForm").innerHTML ="In-Print Stock error!";
        error = 1;
    }
    else if (!formats[0].checked && !formats[1].checked){
        $("#booksubmit").append("Format blank!");
        error = 1;
    }
    if (error == 0){
    // Request to python
        sendReq("/cgi-bin/updatebook.py?" + data + "&mode=update&oldisbn=" + oldisbn, function processResponse(response) {
           $("#bookinfo").append(response); 
           if (response == -1) {
               $("#bookinfo").append("<p>Sorry, wrong password.</p>");
           } else {          
              $("#bookinfo").empty();                         
              $("#bookinfo").append("<p>Success! Information updated.</p>");          
           }        
        });
    }
    
}
/*Deletes a book from the database*/
function deleteBookInfo(oldisbn) {  
   data = $("#booksubmit").serialize();
    
    sendReq("/cgi-bin/updatebook.py?" + data + "&oldisbn=" + oldisbn, function processResponse(response) {
       $("#bookinfo").append(response); 
       if (response == -1) {
           $("#bookinfo").append("<p>Sorry, wrong password.</p>");
       } else {          
          $("#bookinfo").empty();           
          
           $("#bookinfo").append("<p>Success! Book deleted.</p>");          
       }        
    });
}
/*Loads the order info for the order confirmation page. This is simply the
latest order the customer has placed (since this page comes up right after
clicking the send order button*/
function loadOrderInfo() {    
    sendReq("/cgi-bin/latestorder.py", function processResponse(response) {
        
       $("#orderinfo").append("<p>Thank you! Order #" + response + " has been completed! Expect any physical books to be delivered within 3 to 5 business days.</p>");        
        $("#orderinfo").append("<p>Please refer to this order number if you contact us with any issues.</p>");
         $("#orderinfo").append('<a class="btn btn-default cart" href="history.html">Order History</a>');
        $("#orderinfo").append('<a class="btn btn-default cart" href="shop.html">Continue Shopping</a>');
    });
}
/*Loads a selected address on the manage addresses page (auto-populates the address form with
data base on the current active choice in the select query*/
function loadAddressSelection() { 
    
    sendReq("/cgi-bin/loadaddresses.py", function processResponse(response) {  
       $("#editheader").after(response);                
        populateAddress($("#userAddress option:first").val());
       $("#userAddress").on('change', function(e) {           
           var valueSelected = this.value;
           populateAddress(valueSelected);           
       });
       $("#target option:first").attr('selected','selected');
    });
}
/*Populates the addresses on the manage addresses page with the customer's currently stored addresses*/
function populateAddress(addressString) {      
    sendReq("/cgi-bin/getaddressid.py?address=" + addressString, function processResponse(response) {            
        var split = response.split(',');
        id = split[0];
        street = split[1];
        city = split[2];
        state = split[3]
        zip = split[4];
        $("#editstreet").val(street);
        $("#editcity").val(city);
        $("#editstate").val(state);
        $("#editzip").val(zip);
        $("#editsubmit").click(function() {
            editAddress(id, $("#editstreet").val(), $("#editcity").val(), $("#editstate").val(), $("#editzip").val(), true);
        });
        $("#deleteaddress").click(function() {
            editAddress(id, $("#editstreet").val(), $("#editcity").val(), $("#editstate").val(), $("#editzip").val(), false);
        });
        
    });
    
}
/*Updates the user's address. The keepAddress is true when the user clicks edit Address on the manage addresses
page, and false when they click delete address*/
function editAddress(id, street, city, state, zip, keepAddress) {
   form = "id=" + id + "&keep=" + keepAddress + "&street=" + street + "&city=" + city + "&state=" + state + "&zip=" + zip;
    sendReq("/cgi-bin/editaddress.py?" + form, function processResponse(response) { 
        window.location.href = 'addresses.html';
    });
    
}
/*Adds to the user's order*/
function addToOrder() {
    var total = $("#totalVal").val(), address = $("#userAddress").val()
    
    sendReq("/cgi-bin/createOrder.py?total=" + total + "&address=" + address, function processResponse(response) {
        window.location.href = 'orderconfirm.html';
        
    });
}
/*Loads the cart items and user addresses for checkout*/
function loadCheckoutInfo() {
    "use strict";

    // Request to python
    sendReq("/cgi-bin/checkout.py?", function processResponse(response) {
        $("#checkoutItems").append(response);                       
        if ($("#userAddress option").size() == 0) {            
            $("#submitOrder").attr("disabled", true);
            $("#submitOrder").before("<p>Please go to Manage Addresses and add an address before completing your order, then reload this screen.</p>");
        }
    });
}
/*Checks for a valid zip code (5-digit)*/
function testZip(input) { // validation function for username
    var regex = /^\d{5}$/;
    return regex.test(input);
}
/*Used when user clicks on add address on the manage address page*/
function addAddress() {
    "use strict";
    
    var state = $("#state").val(), street = $("#street").val(), city = $("#city").val(), zip = $("#zip").val();
    var error = 0;
    
    if (street == ''){
        document.getElementById("addressForm").innerHTML ="Street error!";
        error = 1;
    }
    else if (city == ''){
        document.getElementById("addressForm").innerHTML ="City error!";
        error = 1;
    }
    else if (!testZip(zip)){
        document.getElementById("addressForm").innerHTML ="Zip code error!";
        error = 1;
    }    
    if (error == 0){
    // Request to python
        sendReq("/cgi-bin/addAddress.py?street=" + street + "&state=" + state + "&city=" + city + "&zip=" + zip, function processResponse(response) {
           document.getElementById("addressForm").innerHTML = response;
        });
    }
}
/*Clones a text input, such as for authors or genres. Used when inputting or editing books*/
var addBox = function(fieldElem) {
  var newBox = fieldElem.prevAll("input").first().clone();
  fieldElem.before(newBox);
};

/*Checks to see which content divs exist on a particular page.
    The functions called depends on the existing content dvs*/
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
    if ($("#editaddress").length) { 
        $("#submitAddress").click(function() {
            addAddress(); 
        });
        loadAddressSelection();        
    }
    if ($("#checkoutItems").length) {
        loadCheckoutInfo();   
    }
    
    //Validates the user's cookies
    validate();
};
