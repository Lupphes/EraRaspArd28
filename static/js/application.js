jQuery(document).ready(function ($) {
    //connect to the socket server.
    var socket = io.connect("http://" + document.domain + ":" + location.port + "/values");
    var numbersReceived = [];

    //receive details from server
    socket.on("newdata", function (msg) {
        //maintain a list of ten numbers
        numbersReceived.push(msg.tempIn);
        numbersReceived.push(msg.tempOut);
        numbersReceived.push(msg.soil);
        numbersReceived.push(msg.humidity);
        numbersReceived.push(msg.light);
        $("#tempIn").html(msg.tempIn);
        $("#tempOut").html(msg.tempOut);
        $("#soil").html(msg.soil);
        $("#humidity").html(msg.humidity);
        $("#lightIntensity").html(msg.light);
    });

});