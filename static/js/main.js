/* globals Cookies, netlify, URLSearchParams */
$(document).ready(function(){

    var login_user_el = $('.login-user');
    var logout_user_el = $('.user-logout');

    var urlParams = new URLSearchParams(location.search);
    var formSubmitted = urlParams.get('form_submitted');
    if(formSubmitted==='True'){
        $('.form-submission-popup').css('display', 'block');
    }

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

    function check_user_authenticated_or_not() {
        if(Cookies.get('authenticated')){
            modify_html_elements('none', 'none', 'block');
        }
    }

    function get_error_message(oauth_provider, err){
        return 'Error Authenticating with ' + oauth_provider + '. ' + err +
            '. Please try again later!';
    }

    function display_error_message(oauth_provider, error_info) {
        $('.error-message').text(get_error_message(oauth_provider, error_info));
        $('.oauth-error').css('display', 'block');
    }

    function modify_html_elements(popup_form_display, login_option_display,
                                  logout__option_display) {
        $('.form-popup').css('display', popup_form_display);
        login_user_el.css('display', login_option_display);
        logout_user_el.css('display', logout__option_display);
    }

    function manipulate_web_page_data(oauth_provider, http_response_text) {
        var json_data = JSON.parse(http_response_text);
        if (json_data.valid) {
            // Cookies expires in 3 days
            Cookies.set('authenticated', true, {expires: 3});
            Cookies.set('username', json_data.user, {expires: 3});
            modify_html_elements('none', 'none', 'block');
        }
        else {
            display_error_message(oauth_provider, json_data.message);
        }
    }

    function validate_user(oauth_provider, access_token){
        var url = 'https://webservices.coala.io/'+ oauth_provider + '/' +
            access_token +'/validate';
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState === 4 && this.status === 200) {
                manipulate_web_page_data(oauth_provider, this.responseText);
            }
        };
        xhttp.open("GET", url, true);
        xhttp.send();
    }

    function login_with(oauth_provider){
        var authenticator = new netlify.default({});
        authenticator.authenticate(
            {
                provider:oauth_provider,
                scope: oauth_provider==='github'?"user":"api"
            }, function(err, data) {
                if(err){
                    display_error_message(oauth_provider, err);
                }
                else {
                    validate_user(data.provider, data.token);
                }
            }
        );
    }

    activate_dropdown();

    check_user_authenticated_or_not();

    $('.sidenav').sidenav();
    $('select').formSelect();

    $(window).resize(function(){
        activate_dropdown();
    });

    $('#current-year').html(new Date().getFullYear());

    login_user_el.click(function () {
        $('.form-popup').css('display', 'block');
    });

    $('.close-form').click(function () {
        $('.form-popup').css('display', 'none');
        $('.form-submission-popup').css('display', 'none');
        $('.oauth-error').css('display', 'none');
    });

    logout_user_el.click(function () {
        Cookies.remove('authenticated');
        Cookies.remove('username');
        modify_html_elements('none', 'block','none');
    });

    $('.login-with-github').click(function(e) {
        e.preventDefault();
        login_with('github');
    });

    $('.login-with-gitlab').click(function(e) {
        e.preventDefault();
        login_with('gitlab');
    });
});
