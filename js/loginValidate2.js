function validate() {

        if ( document.cookie )
        {
            var pairs  = document.cookie.split("; ");
            // Now split each pair on '='.  Check if have a match
            for (var i=0; i < pairs.length; i++) {
               var aPair = pairs[i];
               // split into desired parts and check for match
               var cookieTokens = aPair.split("=");
               var id  = cookieTokens[0];
               var value = cookieTokens[1];
                value = unescape(value);
                alert(id+": " + value);
            }
            //alert("userid: " + userID + "access: " + access);
        }
        else {
           // if there was no cookie then ask the user to input a name
            alert('hello2');
        }
        
        /*if (response == 0) {
            document.getElementById("navbar").innerHTML = "<ul class='nav navbar-nav'><li><a href='itementry.html'><i class='fa fa-shield'></i> Admin</a></li><li><a href='account.html'><i class='fa fa-user'></i> Account</a></li><li><a href='checkout.html'><i class='fa fa-crosshairs'></i> Checkout</a></li><li><a href='cart.html'><i class='fa fa-shopping-cart'></i> Cart</a></li><li><a href='#' class='active'><i class='fa fa-lock'></i> Logout</a></li></ul>";
            
            // change to home screen on successful login attempt
            // window.location = 'index.html';
        } else if (response == 1) { // give invalid login error message
            document.getElementById("error").innerHTML = "Your username or password are invalid. Login Failed.";
        }*/
}

window.onload = function () {
    "use strict";
    // Set onClick for input button
    $("#loginSubmit").click(function () { validate(); });
};
