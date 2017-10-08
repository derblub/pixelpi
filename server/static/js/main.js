$(document).ready(function(){
    $('.pixel').on('change', 'input', function(){
        var $this = $(this),
            value = $this.val();
        console.log(value);
        $this.parent('td').css('background-color', value);
    });


   var ws = new WebSocket('ws://127.0.0.1:9010');
    ws.onopen = function(){
        console.log('Connected to ws://127.0.0.1:9010');
    };
    ws.addEventListener("message", function(event) {
        console.log('Received: ', JSON.parse(event.data));
    });

    sendMessage = function(text){
        console.log('Sent: ' + text);
        ws.send(text);
    }

});