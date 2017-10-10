$(document).ready(function(){

    var ws = new WebSocket('ws://127.0.0.1:9010');
    ws.onopen = function(){
        enableKeys();
        $('#socket-status').removeClass('label-default label-success label-danger')
            .addClass('label-success')
            .text('online');
    };
    ws.onerror = function(){
        clearScreen();
        disableKeys();
        $('#socket-status').removeClass('label-default label-success label-danger')
            .addClass('label-danger')
            .text('error');
    };
    ws.onclose = function(){
        clearScreen();
        disableKeys();
        $('#socket-status').removeClass('label-default label-success label-danger')
            .addClass('label-default')
            .text('offline');
    };
    ws.addEventListener("message", function(event) {
        var data = JSON.parse(event.data);
        updateScreen(data.pixel);

    });

    var updateScreen = function(pixel){
      for (var x=0; x<pixel.length; x++){  // rows
          for (var y=0; y<pixel[x].length; y++){  // col
              var id = '#pixel-'+y+'-'+x,
                  p = pixel[x][y];
              $(id).css('background-color', rgbToHex(p[0], p[1], p[2]));
          }
      }
    };

    var clearScreen = function(){
      $('.pixel').css('background-color', '#000000');
    };

    var disableKeys = function(){
        $('.send-key').attr('disabled', true);
    };

    var enableKeys = function(){
        $('.send-key').removeAttr('disabled');
    };

    $('body').on('click', '.send-key', function(e){
        var $this = $(this),
            key = $this.data('key'),
            json = JSON.stringify({'key': key});
        e.preventDefault();
        ws.send(json);
    });


    function componentToHex(c) {
        var hex = c.toString(16);
        return hex.length === 1 ? "0" + hex : hex;
    }

    function rgbToHex(r, g, b) {
        return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
    }

    $('body').on('click', '.fullscreen', toggleFullscreen);

    function toggleFullscreen() {
        if ((document.fullScreenElement && document.fullScreenElement !== null) ||
           (!document.mozFullScreen && !document.webkitIsFullScreen)) {
            if (document.documentElement.requestFullScreen) {
              document.documentElement.requestFullScreen();
            } else if (document.documentElement.mozRequestFullScreen) {
              document.documentElement.mozRequestFullScreen();
            } else if (document.documentElement.webkitRequestFullScreen) {
              document.documentElement.webkitRequestFullScreen(Element.ALLOW_KEYBOARD_INPUT);
            }
          } else {
            if (document.cancelFullScreen) {
              document.cancelFullScreen();
            } else if (document.mozCancelFullScreen) {
              document.mozCancelFullScreen();
            } else if (document.webkitCancelFullScreen) {
              document.webkitCancelFullScreen();
            }
        }
    }

});