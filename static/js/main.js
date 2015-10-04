$(document).ready(function(){
    $('.pixel').on('change', 'input', function(){
        var $this = $(this),
            value = $this.val();
        console.log(value);
        $this.parent('td').css('background-color', value);
    });
});