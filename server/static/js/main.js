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
        var data = JSON.parse(event.data);
        updateScreen(data.pixel);

    });

    sendMessage = function(text){
        console.log('Sent: ' + text);
        ws.send(text);
    };

    updateScreen = function(pixel){
      for (var x=0; x<pixel.length; x++){  // rows
          for (var y=0; y<pixel[x].length; y++){  // col
              var id = '#pixel-'+y+'-'+x+' input',
                  p = pixel[x][y];
              $(id).val(rgbToHex(p[0], p[1], p[2]));
              $(id).trigger('change');
          }
      }
    };


    function componentToHex(c) {
        var hex = c.toString(16);
        return hex.length === 1 ? "0" + hex : hex;
    }

    function rgbToHex(r, g, b) {
        return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
    }

});