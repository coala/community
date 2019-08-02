$(document).ready(function () {
  var program_selector = $('select#program');
  program_selector.on('change', function () {
    var page_name = program_selector.val();
    $('.page-name').text(page_name);
    if(page_name.search('Summer') > 0){
      $('.gsoc-mentors').css('display', 'flex');
      $('.gci-mentors').css('display', 'none');
    }
    else if(page_name.search('Code-In') > 0){
      $('.gsoc-mentors').css('display', 'none');
      $('.gci-mentors').css('display', 'flex');
    }
  });
});
