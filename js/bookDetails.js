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
}

function addToCart() {
    data = $("#addToCart").serialize();
    
    sendReq("/cgi-bin/addItemCart.py?" + data, function processResponse(response) {
        window.location.href = 'cart.html';        
    });
}
function ensureFormatChecked() {    
    var atLeastOneIsChecked = $('input[name="format[]"]:checked').length > 0;   
    return atLeastOneIsChecked;
}
function enableAddToCart(boxChecked) {    
    $("#addCart").attr("disabled", !boxChecked);
    if (!boxChecked) {
      $("#addCart").after("<p id='hint'>Select one or more formats to be able to add to the cart</p>");    
    } else {
      $("#hint").remove();
    }
    
}
function load() {
    "use strict";
    var parts = window.location.search.substr(1).split("&");
    var $_GET = {};
    for (var i = 0; i < parts.length; i++) {
        var temp = parts[i].split("=");
        $_GET[decodeURIComponent(temp[0])] = decodeURIComponent(temp[1]);
    }

    //alert($_GET['isbn']);
    
    var isbn = $_GET['isbn'];
    // Request to python
    sendReq("/cgi-bin/detail.py?isbn=" + isbn, function processResponse(response) {
        document.getElementById("product").innerHTML = response;
        enableAddToCart(ensureFormatChecked());
        $('input[type=checkbox]').on("click", function() {
            enableAddToCart(ensureFormatChecked());
        });
    });

}

load();
