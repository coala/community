/* globals Cookies */
$(document).ready(function () {

  var community_google_form_op = $('.community-google-form-op');
  var newcomer_promotion_form_op = $('.newcomer-promotion-form-op');
  var calendar_event_form_op = $('.calendar-event-form-op');
  var get_issue_assigned_form_op = $('.get-issue-assigned-form-op');
  var participated_in_gsoc_form_op = $('.participated-in-gsoc-form-op');
  var mentor_students_form_op = $('.mentor-students-form-op');
  var feedback_form_op = $('.feedback-comment');

  var community_google_form = $('.community-google-form');
  var newcomer_promotion_form = $('.newcomer-promotion-form');
  var calendar_event_form = $('.calendar-event-form');
  var get_issue_assigned_form = $('.get-issue-assigned-form');
  var participated_in_gsoc_form = $('.participated-in-gsoc-form');
  var mentor_students_form = $('.mentor-students-form');
  var feedback_form = $('.feedback');

  var is_user_authenticated = Cookies.get('authenticated');
  var authenticated_username = Cookies.get('username');

  var username_input = $('[name$=user]').add($('.newcomer-promotion-form' +
    ' [name$=username]'));
  username_input.attr('value', authenticated_username || 'Anonymous User');
  username_input.attr('disabled', true);

  $('.community-form form').attr(
    'action',window.location.pathname +
                   '?form_submitted=True&form_type=community'
  );

  $('.feedback-form').attr(
    'action',window.location.pathname +
                   '?form_submitted=True&form_type=feedback'
  );

  $.getJSON("/static/contributors-data.json", function (data) {
    var contributor_data = data[authenticated_username];
    var teams = contributor_data.teams;
    if(teams.length === 1){
      community_google_form_op.get(0).remove();
      calendar_event_form_op.get(0).remove();
      mentor_students_form_op.get(0).remove();
      community_google_form.get(0).remove();
      calendar_event_form.get(0).remove();
      mentor_students_form.get(0).remove();
    }
  });

  function display_error_message(message){
    if(message){
      $('.important-message').text(message);
    }
    else {
      $('.important-message').text('You tried to open a form, which is ' +
          'available to only authenticated users. Please join the community' +
          ' or Login(if already a member of organization)');
    }
    $('.form-submission-popup').css('display', 'flex');
  }

  function display_form_or_error(form_object){
    if(is_user_authenticated && authenticated_username){
      $('.community-form').css('display', 'flex');
      form_object.css('display', 'block');
    }
    else {
      display_error_message();
    }
  }

  community_google_form_op.on('click', function () {
    display_form_or_error(community_google_form);
  });

  newcomer_promotion_form_op.on('click', function () {
    display_form_or_error(newcomer_promotion_form);
  });

  calendar_event_form_op.on('click', function () {
    display_form_or_error(calendar_event_form);
  });

  get_issue_assigned_form_op.on('click', function () {
    display_form_or_error(get_issue_assigned_form);
  });

  participated_in_gsoc_form_op.on('click', function () {
    display_form_or_error(participated_in_gsoc_form);
  });

  mentor_students_form_op.on('click', function () {
    display_form_or_error(mentor_students_form);
  });

  feedback_form_op.on('click', function () {
    feedback_form.css('display', 'block');
    $('.user-feeling-level i').on('click', function () {
      var experience = $(this).attr('experience');
      $('input[name="experience"]').val(experience);
      $('.user-feeling-level i').css('color', 'black');
      if(experience==='Negative'){
        $(this).css('color', 'red');
      }
      else if(experience==='Neutral'){
        $(this).css('color', 'blue');
      }
      else {
        $(this).css('color', 'darkgreen');
      }
    });
  });

  $('.community-form :input').focusin(function () {
    if (is_user_authenticated===undefined &&
          authenticated_username===undefined) {
      $('.community-form').css('display', 'none');
      display_error_message();
    }
  });

  $('.user_disabled_input').focusin(function () {
    display_error_message('Sorry! But you are not allowed to change this' +
      ' field value.');
  });
});
