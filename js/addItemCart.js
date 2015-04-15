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

function load() {
    data = $("#booksubmit").serialize();
    
    sendReq("/cgi-bin/addItemCart.py?" + data + "&mode=update", function processResponse(response) {
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

load();
