var $;
function sendReq(url, callbackFunction) {
    "use strict";
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

function validate() {
    "use strict";
    // Get username and year value from form
    var username = $("#username").val(), password = $("#password").val();
    
    // Request to python
    sendReq("/cgi-bin/loginValidate.py?username=" + username + "&password=" + password, function processResponse(response) {
        // enable user nav tabs
        
        if (response == 0) {
            document.getElementById("navbar").innerHTML = "<ul class='nav navbar-nav'><li><a href='itementry.html'><i class='fa fa-shield'></i> Admin</a></li><li><a href='account.html'><i class='fa fa-user'></i> Account</a></li><li><a href='checkout.html'><i class='fa fa-crosshairs'></i> Checkout</a></li><li><a href='cart.html'><i class='fa fa-shopping-cart'></i> Cart</a></li><li><a href='#' class='active'><i class='fa fa-lock'></i> Logout</a></li></ul>";
            
            // change to home screen on successful login attempt
            window.location.href = 'index.html';
        } else if (response == 1) { // give invalid login error message
            document.getElementById("error").innerHTML = "Your username or password are invalid. Login Failed.";
        }
    });
}

window.onload = function () {
    "use strict";
    // Set onClick for input button
    $("#loginSubmit").click(function () { validate(); });
};
