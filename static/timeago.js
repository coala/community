function generateTimeString(timestamp) {
  var sec = ((new Date()).getTime() / 1000) - parseInt(timestamp);
  var min = sec / 60;
  var hour = min / 60;
  var day = hour / 24;

  var timeString = '';
  if (day >= 1) {
    timeString = Math.round(day) + ' days ago';
  } else if (hour >= 1) {
    timeString = Math.round(hour) + ' hours ago';
  } else if (min >= 1) {
    timeString = Math.round(min) + ' minutes ago';
  } else {
    timeString = Math.round(sec) + ' seconds ago';
  }

  return timeString;
}

function updateTimeAgo(time, ago) {
  ago.innerHTML = generateTimeString(time.getAttribute('data-time'));
}

function loadTimeElements() {
  var time = document.getElementById('time');
  var ago = document.getElementById('ago');

  updateTimeAgo(time, ago);
}
