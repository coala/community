/* globals $, Chart */
var curChart;

function setChart(labels, openedData, closedData, type) {
  var ctx = document.getElementById("canvas");

  curChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: "Issues Opened",
        backgroundColor: "RGBA(33, 150, 243, 0.2)",
        borderColor: "RGBA(33, 150, 243, 1)",
        data: openedData,
        fill: true,
      }, {
        label: "Issues Closed",
        backgroundColor: "RGBA(244, 67, 54, 0.2)",
        borderColor: "RGBA(244, 67, 54, 1)",
        data: closedData,
        fill: true,
      }]
    },
    options: {
      responsive: true,
      title: {
        display: true,
        text: 'Community Activity'
      },
      tooltips: {
        mode: 'index',
        intersect: false,
      },
      hover: {
        mode: 'nearest',
        intersect: true
      },
      scales: {
        xAxes: [{
          display: true,
          scaleLabel: {
            display: true,
            labelString: type
          }
        }],
        yAxes: [{
          display: true,
          scaleLabel: {
            display: true,
            labelString: 'Number'
          }
        }]
      }
    }
  });
}

function updateChart(type) {
  if(curChart){ curChart.destroy(); }

  $.getJSON("/static/activity-data.json",
    function(data) {
      var labels, openedData, closedData;
      if(type === "Month") {
        labels = data.year.labels;
        openedData = data.year.opened;
        closedData = data.year.closed;
      }
      else if(type === "Week") {
        labels = data.month.labels;
        openedData = data.month.opened;
        closedData = data.month.closed;
      }
      else {
        labels = data.week.labels;
        openedData = data.week.opened;
        closedData = data.week.closed;
      }
      setChart(labels, openedData, closedData, type);
  })
  .fail(function(data, textStatus, error) {
    var err = textStatus + ", " + error;
    console.error("Request Failed: " + err);
  });
}
