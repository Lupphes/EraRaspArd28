$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect("http://" + document.domain + ":" + location.port + "/test");
    var numbersReceived = [];

    //receive details from server
    socket.on("newnumber", function(msg) {
	console.log("Received number" + msg.number);
        //maintain a list of ten numbers
        numbersReceived.push(msg.number);
        $("#test").html(msg.number);
    });

});
