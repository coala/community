$(document).ready(function () {

  var search_input = $('#search');
  var score_range_selector = $('.score-range-selector');
  var level_selector = $('.level-selector');
  var badge_selector = $('.badge-selector');
  var filter_button = $('.filter-btn .btn-large');

  function toggleGamificationCards(display){
    $('.gamifier-card').css('display', display);
  }

  function toggleFilterButton(disabled){
    if(disabled){
      filter_button.attr('disabled', 'disabled');
    }
    else {
      filter_button.removeAttr('disabled');
    }
  }

  search_input.on('keypress keyup', function () {
    var value = search_input.val();
    if(value){
      toggleFilterButton(true);
    }
    else {
      toggleFilterButton(false);
    }
  });

  $('.fa-close').on('click', function () {
    toggleFilterButton(false);
  });

  function getContributorsBasedOnFilterSelector(id_prefix, filter_option){
    var filtered_users = [];
    if(filter_option.val()){
      var spans = Object.values(
        $('.contributors-cards #'+id_prefix+'-'+filter_option.val())
      );
      if(spans.length > 0){
        spans.forEach(function (span) {
          if(span.attributes !== undefined){
            filtered_users.push(span.attributes.login.value);
          }
        });
      }
    }
    return filtered_users;
  }

  function getCommonContribs(in_range_users, at_level_users, has_badges_users){
    var all_contribs = [];
    if (score_range_selector.val() !== "[]"){
      all_contribs = in_range_users;
    }
    if(level_selector.val() !== ""){
      if (all_contribs.length === 0){
        all_contribs = at_level_users;
      }
      else {
        all_contribs = all_contribs.filter(function(username){
          return at_level_users.includes(username);
          }
        );
      }
    }
    if (badge_selector.val() !== ""){
      if (all_contribs.length === 0){
        all_contribs = has_badges_users;
      }
      else {
        all_contribs = all_contribs.filter(function(username){
          return  has_badges_users.includes(username);
          }
        );
      }
    }
    return all_contribs;
  }

  function filterUsersAndToggleCards(){
    var in_range_users = JSON.parse(score_range_selector.val());
    var at_level_users = getContributorsBasedOnFilterSelector(
      'level', level_selector
    );
    var has_badges_users = getContributorsBasedOnFilterSelector(
      'badge', badge_selector
    );

    if(score_range_selector.val() === "[]" && level_selector.val() === "" &&
       badge_selector.val() === ""){
      toggleGamificationCards('flex');
    }
    else {
      toggleGamificationCards('none');
      var contributors = getCommonContribs(
        in_range_users, at_level_users, has_badges_users
      );

      if(contributors.length > 0){
        $('.no-contribs-found').css('display', 'none');
        contributors.forEach(function (username) {
          $('[login='+username+']').css('display', 'flex');
        });
      }
      else {
        $('.no-contribs-found').css('display', 'flex');
        $('.no-contribs-found .search-message').text(
          'No contributors found for you selected filter(s). Please' +
          ' try different filter options!'
        );
      }
    }
  }

  score_range_selector.on('change', function () {
    filterUsersAndToggleCards();
  });

  level_selector.on('change', function () {
    filterUsersAndToggleCards();
  });

  badge_selector.on('change', function () {
    filterUsersAndToggleCards();
  });

  $('.filter-btn').on('click', function () {
    var filters_option = $('.filters-option');
    var el_display = filters_option.css('display');
    if(el_display === 'flex'){
      filters_option.css('display', 'none');
    }
    else {
      filters_option.css('display', 'flex');
    }
  });

  $('.clear-filters').on('click', function () {
    score_range_selector.val("[]");
    level_selector.val("");
    badge_selector.val("");
    $('select').formSelect();
    $('.no-contribs-found').css('display', 'none');
    toggleGamificationCards('flex');
  });

});