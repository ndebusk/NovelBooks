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

function testZip(input) { // validation function for username
    var regex = /^\d{5}$/;
    return regex.test(input);
}

function add() {
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

$("#submitAddress").click(function() { add(); });
