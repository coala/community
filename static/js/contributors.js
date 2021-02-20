$(document).ready(function(){
    var search_input = $('#search');
    var close_icon = $('.contributors-section .fa-close');
    var results_body = $('.search-results-tbody');
    var searched_keyword = null;
    var contributors_card = $('.contributor-card');

    function appendChildren(element, username, el_result_value,
                            hide_all_contributors){
        var result_td = $('<tr></tr>').text(el_result_value);
        result_td.id = "td-" + username;
        if(hide_all_contributors){
            result_td.on('click', function(){
                var row_id = result_td.id;
                var login = row_id.replace('td-', '');
                $('.contributor-card').css('display', 'none');
                var contrib_card = $('[login=' + login +']');
                if(contrib_card.hasClass('meta-reviewer')){
                    contrib_card.css('display', 'flex');
                }
                else{
                    contrib_card.css('display', 'block');
                }
                $('.search-results').css('display', 'none');
            });
        }
        element.append(result_td);
    }

    function match(search, element, attribute){
        return $(element).attr(attribute).toLowerCase().indexOf(search) > -1;
    }

    search_input.on('keypress keyup', function(){
        searched_keyword = search_input.val().toLowerCase();
        if(searched_keyword === ''){
            $('.search-results').css('display', 'none');
            close_icon.css('display', 'none');
        }
        else {
            $('.search-results').css('display', 'block');
            close_icon.css('display', 'block');
            var all_results = [];
            contributors_card.filter(function () {
                if(match(searched_keyword, this, 'login') ||
                   match(searched_keyword, this, 'name')) {
                    all_results.push($(this));
                }
            });
            var results_tbody_tr = $('.search-results-tbody tr');
            results_tbody_tr.remove();
            if(all_results.length === 0 ){
                appendChildren(results_body, null, 'No results found!', false);
            }
            else {
                all_results.forEach(function (result) {
                    var login = result.attr('login');
                    var name = result.attr('name');
                    var result_value = null;
                    if(name){
                        result_value = login + " (" + name + ")";
                    }
                    else {
                        result_value = login;
                    }
                    appendChildren(results_body, login, result_value, true);
                });
            }
        }
    });

    close_icon.on('click', function(){
        var all_contrib_cards = $('.contributor-card');
        if(all_contrib_cards.hasClass('meta-reviewer')){
            all_contrib_cards.css('display', 'flex');
        }
        else {
            all_contrib_cards.css('display', 'block');
        }
        close_icon.css('display', 'none');
        search_input.val(null);
        $('.search-results').css('display', 'none');
    });
});
