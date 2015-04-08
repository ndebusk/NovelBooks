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

function load() {
    "use strict";
    
    // Request to python
    sendReq("/cgi-bin/loadBooks.py?", function processResponse(response) {
        alert(response);
        document.getElementById("allproducts").innerHTML = response;
    });
}

window.onload = function () {
    "use strict";
    // Set onClick for input button
    load();
};
