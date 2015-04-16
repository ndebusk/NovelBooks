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

function deleteItem() {
    data = $("#cartItem").serialize();
    sendReq("/cgi-bin/deleteCartItem.py?" + data, function processResponse(response) {
        window.location.href = 'cart.html';  
    });
}

function load() {
    "use strict";

    // Request to python
    sendReq("/cgi-bin/loadcart.py?", function processResponse(response) {
        document.getElementById("cart_items").innerHTML = response;
    });
}

load();
