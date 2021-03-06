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

function addToOrder() {
    var total = $("#totalVal").val(), address = $("#userAddress").val()
    
    sendReq("/cgi-bin/createOrder.py?total=" + total + "&address=" + address, function processResponse(response) {
        window.location.href = 'orderconfirm.html';
        
    });
}

function load() {
    "use strict";

    // Request to python
    sendReq("/cgi-bin/checkout.py?", function processResponse(response) {
        document.getElementById("checkoutItems").innerHTML = response;  
        alert($("#useraddress option").size());
        if ($("#useraddress option").size() == 0) {            
            $("#submitOrder").attr("disabled", true);
            $("#submitOrder").before("<p>Please go to Manage Addresses and add an address before completing your order, then reload this screen.</p>");
        }
    });
}

load();
