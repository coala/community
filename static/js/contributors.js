$(document).ready(function(){
    var search_input = $('#search');
    var close_icon = $('.contributors-section .fa-close');
    var results_body = $('.search-results-tbody');
    var searched_keyword = null;

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

    search_input.on('keypress keyup', function(){
        searched_keyword = search_input.val();
        if(searched_keyword === ''){
            $('.search-results').css('display', 'none');
            close_icon.css('display', 'none');
        }
        else {
            $('.search-results').css('display', 'block');
            close_icon.css('display', 'block');
            var search_by_login = $(
              '.contributor-card[login^=' + searched_keyword +']'
            );
            var search_by_name = $(
              '.contributor-card[name^=' + searched_keyword +']'
            );
            var results_tbody_tr = $('.search-results-tbody tr');
            results_tbody_tr.remove();
            if(search_by_login.length + search_by_name.length === 0 ){
                appendChildren(results_body, null, 'No results found!', false);
            }
            else {
                var all_results = search_by_login.add(search_by_name);
                for(var contrib in all_results.get()){
                    if(all_results[contrib]){
                        var login = all_results[contrib].getAttribute('login');
                        var name = all_results[contrib].getAttribute('name');
                        var result_value = null;
                        if(name){
                            result_value = login + " (" + name + ")";
                        }
                        else {
                            result_value = login;
                        }
                        appendChildren(results_body, login, result_value, true);
                    }
                }
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
