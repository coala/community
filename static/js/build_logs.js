$(document).ready(function(){
    $('select').formSelect();

    var log_chooser_input = $('#log-chooser-input');
    var search_input = $('#search');
    var search_icon = $('.build-logs-section .small-screen');
    var close_icon = $('.build-logs-section .fa-close');
    var log_chooser_div = $('.build-logs-section .log-chooser');
    var search_field_div = $('.build-logs-section .search-field');
    var log_type = null;
    var logs_data = null;
    var searched_keyword = '';

    function addLogsHTML(info){
        var info_el = $('<p></p>').text(info);
        $('.build-logs').append(info_el);
    }

    function updateBuildLogsHTML(){
        $('.build-logs p').remove();
        if(logs_data.length > 0) {
            for(var entry in logs_data){
                if(logs_data[entry]){
                    addLogsHTML(logs_data[entry]);
                }
            }
        }
        else {
            var info = 'There are no log entries for tag ' + log_type + '.';
            addLogsHTML(info);
        }
    }

    function updateBuildLogs(type){
        $.getJSON("/static/ci-build-detailed-logs.json", function(data) {
            log_type = type;
            if(log_type === 'logs') {
                logs_data = data[log_type];
            }
            else {
                logs_data = data.logs_level_Specific[log_type];
            }
            updateBuildLogsHTML();
        })
        .fail(function(data, textStatus, error) {
            var err = "Request Failed: " + textStatus + ", " + error;
            console.error(err);
        });
    }

    function searchBuildLogs(){
        var found = false;
        var info = '';
        for(var entry in logs_data){
            if(logs_data[entry]){
                info = logs_data[entry];
                if(info.includes(searched_keyword)){
                    found = true;
                    addLogsHTML(info);
                }
            }
        }
        if(!found){
            if(log_type === 'logs'){
                info = searched_keyword + ' not found in logs!';
            }
            else {
                info = searched_keyword + ' not found in ' + log_type +
                ' level logs!';
            }
            addLogsHTML(info);
        }
    }

    updateBuildLogs('logs');

    log_chooser_input.on('change', function(){
        updateBuildLogs(log_chooser_input.val());
    });

    search_input.on('keypress', function(key){
        if(key.which === 13){
            searched_keyword = search_input.val();
            $('.build-logs p').remove();
            searchBuildLogs();
        }
    });

    search_icon.on('click', function(){
        search_icon.css('display', 'none');
        close_icon.css('display', 'block');
        log_chooser_div.css('display', 'none');
        search_field_div.css('display', 'flex');
    });
    close_icon.on('click', function(){
        search_icon.css('display', 'flex');
        close_icon.css('display', 'none');
        log_chooser_div.css('display', 'flex');
        search_field_div.css('display', 'none');
    });

});
