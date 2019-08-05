$(document).ready(function(){
    function activate_dropdown(){
        if ($('nav').width() < 992 ){
            $(".dropdown-trigger-sidenav").dropdown({coverTrigger: false});
        }
        else {
            $(".dropdown-trigger").dropdown({hover: true,
                                             constrainWidth: false,
                                             coverTrigger: false});
        }
    }

    activate_dropdown();

    $('.sidenav').sidenav();
    $('select').formSelect();

    $(window).resize(function(){
        activate_dropdown();
    });

    $('#current-year').html(new Date().getFullYear());
});
