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

function add() {
    "use strict";
    var data = $("#itemForm").serialize();
    var isbn = $("#isbn").val(), 
        title = $("#booktitle").val(), 
        publisher = $("#publisher").val(), 
        price = $("#price").val(), 
        pages = $("#pagenum").val(), 
        description = $("#description").val(), 
        image = $("#bookimage").val(), 
        authors = document.getElementsByName('author[]'), 
        formats = document.getElementsByName('format[]'), 
        genres = document.getElementsByName('genre[]'),
        inStock = $("#instock").val();
    var error = 0;
    if (isbn == '' || isbn.length != 13 || isNaN(isbn)){
        document.getElementById("newItemForm").innerHTML ="ISBN error, must be 13-digits!";
        error = 1;
    }
    else if (title == ''){
        document.getElementById("newItemForm").innerHTML ="Title blank!";
        error = 1;
    }
    else if (publisher == ''){
        document.getElementById("newItemForm").innerHTML ="Publisher blank!";
        error = 1;
    }
    else if (price == '' || isNaN(price)){
        document.getElementById("newItemForm").innerHTML ="Price error!";
        error = 1;
    }
    else if (pages == '' || isNaN(pages)){
        document.getElementById("newItemForm").innerHTML ="Pages error!";
        error = 1;
    }
    else if (description == ''){
        document.getElementById("newItemForm").innerHTML ="Description blank!";
        error = 1;
    }
    else if (image == ''){
        document.getElementById("newItemForm").innerHTML ="Provide Image file path!";
        error = 1;
    }
    else if (authors[0].value == ''){
        document.getElementById("newItemForm").innerHTML ="Author blank!";
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
        document.getElementById("newItemForm").innerHTML ="Format blank!";
        error = 1;
    }
    
    if (error == 0){
    // Request to python
        sendReq("/cgi-bin/itementry.py?" + data, function processResponse(response) {
            document.getElementById("newItemForm").innerHTML = response;
        });
    }
}
var addBox = function(fieldElem) {
  var newBox = fieldElem.prevAll("input").first().clone();
  fieldElem.before(newBox);
};

$(document).ready(function () {    
    $(".expanderbutton").click(function () {        
        addBox($(this));  
    });

$("#saveBook").click(function() { add(); });    

$("#editBookSubmit").click(function() {
           window.location.href = 'editbook.html';    
        });     
});
