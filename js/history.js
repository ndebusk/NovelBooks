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
    sendReq("/cgi-bin/history.py?", function processResponse(response) {
        document.getElementById("orderList").innerHTML = response;
    });
}

load();
