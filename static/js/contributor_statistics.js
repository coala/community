/* globals Chart, Map, Set */
$(document).ready(function () {
  var hoster_selector = $('#hoster-selector');
  var stats_divider = $('#stats-divider');
  var user_statistics_display = $('.user-statistics');
  var commitsChart, reviewsChart, issuesChart, mergeRequestsChart;
  var commits_canvas = $('#commits-canvas');
  var issues_canvas = $('#issues-canvas');
  var merge_requests_canvas = $('#merge-requests-canvas');
  var reviews_canvas = $('#reviews-canvas');
  var repository_stats_canvas = $('#repository-stats-canvas');
  var month_names = ["January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
  ];

  function displayDataUpdatedDates(data) {
    var user_data_updated_dates = data.updated_at;
    var user_updated_el = $('.user-updated-datetime');
    user_updated_el.empty();
    var gh_date = new Date(user_data_updated_dates.github);
    var gl_date = new Date(user_data_updated_dates.gitlab);
    var last_fetched_gh_data_el = $('<p><strong></strong></p>').text(
      'GitHub: ' + gh_date.toUTCString());
    var last_fetched_gl_data_el = $('<p><strong></strong></p>').text(
      'GitLab: ' + gl_date.toUTCString());
    user_updated_el.append(last_fetched_gh_data_el);
    user_updated_el.append(last_fetched_gl_data_el);
    user_updated_el.css('justify-content', 'space-evenly');
  }

  function displayWorkingOnIssuesCount(data) {
    var on_hoster_counts = data.working_on_issues_count;
    var count_list_el = $('.count-list');
    count_list_el.empty();
    var github_issue_count_el = $('<li></li>').text('GitHub: ' +
                                                    on_hoster_counts.github);
    var gitlab_issue_count_el = $('<li></li>').text('GitLab: ' +
                                                    on_hoster_counts.gitlab);
    count_list_el.append(github_issue_count_el);
    count_list_el.append(gitlab_issue_count_el);
  }

  function setLabelCSSProperties(label_element, bg_color){
      label_element.css('background-color', bg_color);
      label_element.css('color', 'white');
      label_element.css('border-radius', '10px');
      label_element.css('margin', '0 3px');
      label_element.css('padding', '5px');
      return label_element;
  }

  function displayWorkedOnIssueLabels(data) {
    var issue_labels = data.type_of_issues_worked_on;
    var gh_issue_labels_el = $('.github-issue-labels');
    var gl_issue_labels_el = $('.gitlab-issue-labels');
    gh_issue_labels_el.empty();
    gl_issue_labels_el.empty();
    jQuery.each(issue_labels.github, function (label_name, color) {
      var label_el = $('<p></p>').text(label_name);
      label_el = setLabelCSSProperties(label_el, '#'+color);
      gh_issue_labels_el.append(label_el);
    });
    jQuery.each(issue_labels.gitlab, function (label_name, color) {
      var label_el = $('<p></p>').text(label_name);
      label_el = setLabelCSSProperties(label_el, color);
      gl_issue_labels_el.append(label_el);
    });
  }

  function get_options(title) {
    return {
      responsive: true,
      maintainAspectRatio: false,
      fill: true,
      borderWidth: 3,
      title: {
        display: true,
        text: title
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
          stacked: true,
          display: true,
          scaleLabel: {
            display: true,
          }
        }],
        yAxes: [{
          stacked: true,
          display: true,
          scaleLabel: {
            display: true,
            labelString: 'Number'
          }
        }]
      }
    };
  }

  function get_dataset_properties(label, backgroundColor, data){
    return {
      label: label,
      backgroundColor: backgroundColor,
      data: data,
    };
  }

  function setRepositoryCanvasChart(stats) {
    new Chart(repository_stats_canvas, {
      type: 'bar',
      data: {
        labels: stats.repositories,
        datasets: [
          get_dataset_properties("Commits", "RGBA(236,255,52,0.7)",
                                 stats.commits),
          get_dataset_properties("Reviews", "RGBA(236,151,52,0.7)",
                                 stats.reviews),
          get_dataset_properties("Issues Opened", "RGBA(178, 191, 0, 0.7)",
                                 stats.issues_opened),
          get_dataset_properties("Issues Assigned", "RGBA(178, 52, 237, 0.7)",
                                 stats.assigned_issues),
          get_dataset_properties("Issues Closed", "RGBA(255, 52, 61, 0.7)",
                                 stats.issues_closed),
          get_dataset_properties("Merge Requests Opened", "RGBA(255, 190," +
            " 217, 0.7)", stats.merge_requests_opened),
          get_dataset_properties("Unmerged Merge Requests", "RGBA(87, 190," +
            " 138, 0.7)", stats.unmerged_merge_requests),
          ]
      },
      options: get_options('Repository-Wise Statistics')
    });
  }

  function setCommitsAndReviewsChart(commitLabels, commitData,
                                     reviewLabels, reviewData) {

    commitsChart = new Chart(commits_canvas, {
      type: 'bar',
      data: {
        labels: commitLabels,
        datasets: [
          get_dataset_properties("Commits Activity", "RGBA(87, 190, 217," +
            " 0.7)", commitData)
        ]
      },
      options: get_options('Commits Activity')
    });

    reviewsChart = new Chart(reviews_canvas, {
      type: 'bar',
      data: {
        labels: reviewLabels,
        datasets: [
          get_dataset_properties("Reviews Activity", "RGBA(87, 190, 138," +
            " 0.7)", reviewData)
        ]
      },
      options: get_options('Review Activity'),
    });
  }

  function setIssuesCanvasChart(data){
    var data_labels = new Set();
    jQuery.each(data, function (subtype, display_filters){
      jQuery.each(display_filters, function (filter, value) {
        data_labels.add(filter);
      });
    });
    data_labels.forEach(function (data_label) {
      jQuery.each(data, function (subtype){
        if(isNaN(data[subtype][data_label])){
          data[subtype][data_label] = 0;
        }
      });
    });
    data_labels = Array.from(data_labels);
    issuesChart = new Chart(issues_canvas, {
      type: 'bar',
      data: {
        labels: data_labels,
        datasets: [
          get_dataset_properties("Closed Issues Activity","RGBA(87, 190," +
            " 138, 0.7)", Object.values(data.closed)),
          get_dataset_properties("Assigned Issues Activity","RGBA(255, 224," +
            " 217, 0.8)", Object.values(data.assigned)),
          get_dataset_properties("Opened Issues Activity", "RGBA(236, 151," +
            " 52, 0.6)", data.open !== undefined?Object.values(data.open):
            Object.values(data.opened))
        ]
      },
      options: get_options('Issues Activity')
    });
  }

  function setMergeRequestsCanvasChart(data){
    var data_labels = new Set();
    jQuery.each(data, function (subtype, display_filters){
      jQuery.each(display_filters, function (filter, value) {
        data_labels.add(filter);
      });
    });
    data_labels.forEach(function (data_label) {
      jQuery.each(data, function (subtype){
        if(isNaN(data[subtype][data_label])){
          data[subtype][data_label] = 0;
        }
      });
    });
    data_labels = Array.from(data_labels);
    mergeRequestsChart = new Chart(merge_requests_canvas, {
      type: 'line',
      data: {
        labels: data_labels,
        datasets: [
          get_dataset_properties("Merged PRs Activity","RGBA(255, 224, 217," +
            " 0.5)",data.merged !==undefined?Object.values(data.merged):
            new Array(data_labels.size)),
          get_dataset_properties("Unmerged PRs Activity","RGBA(178, 52, 237," +
            " 0.7)", data.unmerged !== undefined?Object.values(data.unmerged):
            new Array(data_labels.size)),
          get_dataset_properties("Opened PRs Activity", "RGBA(236, 151, 52," +
            " 0.9)",  data.open !== undefined?Object.values(data.open):
            (data.opened !== undefined?Object.values(data.opened):
              new Array(data_labels.size)))
        ]
      },
      options: get_options('Merge Requests Activity')
    });
  }

  function setCanvasCharts(data){
    setCommitsAndReviewsChart(
      Object.keys(data.commits), Object.values(data.commits),
      Object.keys(data.reviews), Object.values(data.reviews)
    );
    setIssuesCanvasChart(data.issues);
    setMergeRequestsCanvasChart(data.merge_requests);
  }

  function toggleCanvasDisplays(data){
    if (Object.values(data.reviews).length === 0) {
      $('.bar-reviews-canvas').css('display', 'none');
    }
    else {
      $('.bar-reviews-canvas').css('display', 'block');
    }
    if (Object.values(data.issues).length === 0) {
      $('.bar-issues-canvas').css('display', 'none');
    }
    else {
      $('.bar-issues-canvas').css('display', 'block');
    }
    if (Object.values(data.commits).length === 0) {
      $('.bar-commits-canvas').css('display', 'none');
    }
    else {
      $('.bar-commits-canvas').css('display', 'block');
    }
    if (Object.values(data.merge_requests).length === 0) {
      $('.line-merge-requests-canvas').css('display', 'none');
    }
    else {
      $('.line-merge-requests-canvas').css('display', 'block');
    }
  }

  function getWeekNumber(date) {
    var d = new Date(Date.UTC(date.getFullYear(), date.getMonth(),
      date.getDate()));
    var dayNum = d.getUTCDay() || 7;
    d.setUTCDate(d.getUTCDate() + 4 - dayNum);
    var yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
    return Math.ceil((((d - yearStart) / 86400000) + 1) / 7);
  }

  function getMonthNameFromWeekNumber(year, week_number) {
    var total_ms_count = ((week_number * 7) - 1) * 86400000;
    var current_date = new Date();
    var d = new Date(Date.UTC(year, current_date.getMonth(),
      current_date.getDate()));
    var dayNum = d.getUTCDay() || 7;
    d.setUTCDate(d.getUTCDate() + 4 - dayNum);
    var yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
    var date = new Date(total_ms_count + yearStart.getTime());
    return month_names[date.getMonth()];
  }

  function get_last_twelve_months_begin_end_weeks() {
    var current_date = new Date();
    var last_year_date = new Date(
      current_date.getFullYear() - 1, current_date.getMonth(),
      current_date.getDate()
    );
    return [current_date.getFullYear(), getWeekNumber(current_date),
      getWeekNumber(last_year_date)];
  }

  function get_last_twelve_weeks_begin_end() {
    var current_date = new Date();
    var current_week = getWeekNumber(current_date);
    var last_twelfth_week = 1;
    if (current_week > 12) {
      last_twelfth_week = current_week - 12;
    } else {
      var week_difference = 12 - current_week;
      var month = Math.trunc((11 - week_difference) / 4);
      var last_year_date = new Date(
        current_date.getFullYear() - 1, month,
        current_date.getDate());
      last_twelfth_week = getWeekNumber(last_year_date);
    }
    return [current_date.getFullYear(), current_week, last_twelfth_week];
  }

  function updateCharts(data, hoster_type, display_type) {
    if(commitsChart){
      commitsChart.destroy();
      reviewsChart.destroy();
      issuesChart.destroy();
      mergeRequestsChart.destroy();
    }
    var hoster_stats = data.statistics[hoster_type];
    var charts_data = {
      issues: new Map(),
      commits: new Map(),
      merge_requests: new Map(),
      reviews: new Map(),
    };
    var issue_stats, commits_stats, prs_stats, reviews_stats, current_year,
        current_week;
    if (display_type === "yearly") {

      jQuery.each(hoster_stats, function (repo_name, repo_stats) {
        issue_stats = repo_stats.issues;
        jQuery.each(issue_stats, function (issue_type, years) {
          if (charts_data.issues[issue_type] === undefined) {
            charts_data.issues[issue_type] = new Map();
          }
          jQuery.each(years, function (year, week_numbers) {
            jQuery.each(week_numbers, function (
              week_number, weekdays) {
              jQuery.each(weekdays, function (
                weekday, issues) {
                if (isNaN(charts_data.issues[issue_type][year])) {
                  charts_data.issues[issue_type][year] = 0;
                }
                charts_data.issues[issue_type][year] +=
                  Object.keys(issues).length;
              });

            });
          });
        });

        prs_stats = repo_stats.prs || repo_stats.merge_requests;
        jQuery.each(prs_stats, function (pr_type, years) {
          if (charts_data.merge_requests[pr_type] === undefined) {
            charts_data.merge_requests[pr_type] = new Map();
          }
          jQuery.each(years, function (year, week_numbers) {
            jQuery.each(week_numbers, function (
              week_number, weekdays) {
              jQuery.each(weekdays, function (weekday, mrs) {
                if (isNaN(charts_data.merge_requests[pr_type][year])) {
                  charts_data.merge_requests[pr_type][year] = 0;
                }
                charts_data.merge_requests[pr_type][year] +=
                  Object.keys(mrs).length;
              });

            });
          });
        });

        commits_stats = repo_stats.commits;
        jQuery.each(commits_stats, function (year, week_numbers) {
          jQuery.each(week_numbers, function (week_number, weekdays){
            jQuery.each(weekdays, function (weekday, commits_done){
              if (isNaN(charts_data.commits[year])) {
                charts_data.commits[year] = 0;
              }
              charts_data.commits[year] +=
                Object.keys(commits_done).length;
            });
          });
        });

        reviews_stats = repo_stats.reviews;
        jQuery.each(reviews_stats, function (year, week_numbers) {
          jQuery.each(week_numbers, function (week_number, weekdays){
            jQuery.each(weekdays, function (weekday, reviews_done){
              if (isNaN(charts_data.reviews[year])) {
                charts_data.reviews[year] = 0;
              }
              charts_data.reviews[year] +=
                Object.keys(reviews_done).length;
            });
          });
        });
      });
    }

    else if (display_type === "monthly") {
      var last_twelve_months_weeks = get_last_twelve_months_begin_end_weeks();
      current_year = last_twelve_months_weeks[0];
      current_week = last_twelve_months_weeks[1];
      var last_year_week = last_twelve_months_weeks[2];

      jQuery.each(hoster_stats, function (repo_name, repo_stats) {

        issue_stats = repo_stats.issues;
        jQuery.each(issue_stats, function (issue_type, years) {
          if (charts_data.issues[issue_type] === undefined) {
            charts_data.issues[issue_type] = new Map();
          }
          jQuery.each(years, function (year, week_numbers) {
            jQuery.each(week_numbers, function (week_number, weekdays) {
              year = parseInt(year);
              week_number = parseInt(week_number);
              if (
                (current_year === year &&
                  week_number <= current_week) ||
                (year === (current_year - 1) &&
                  week_number >= last_year_week)) {
                jQuery.each(weekdays, function (weekday,
                                                issues) {
                  var month_name
                    = getMonthNameFromWeekNumber(year, week_number);
                  var key = month_name + '\'' + year%100;
                  if (isNaN(charts_data.issues[issue_type][key])) {
                    charts_data.issues[issue_type][key] = 0;
                  }
                  charts_data.issues[issue_type][key] +=
                    Object.keys(issues).length;
                });
              }
            });
          });
        });

        prs_stats = repo_stats.prs || repo_stats.merge_requests;
        jQuery.each(prs_stats, function (pr_type, years) {
          if (charts_data.merge_requests[pr_type] === undefined) {
            charts_data.merge_requests[pr_type] = new Map();
          }
          jQuery.each(years, function (year, week_numbers) {
            jQuery.each(week_numbers, function (week_number, weekdays) {
              year = parseInt(year);
              week_number = parseInt(week_number);
              if ((current_year === year && week_number <= current_week) ||
                (year === (current_year - 1) &&
                  week_number >= last_year_week)) {
                jQuery.each(weekdays, function (weekday, mrs) {
                  var month_name
                    = getMonthNameFromWeekNumber(year, week_number);
                  var key = month_name + '\'' + year%100;
                  if (isNaN(charts_data.merge_requests[pr_type][key])) {
                    charts_data.merge_requests[pr_type][key] = 0;
                  }
                  charts_data.merge_requests[pr_type][key] +=
                    Object.keys(mrs).length;
                });
              }
            });
          });
        });

        commits_stats = repo_stats.commits;
        jQuery.each(commits_stats, function (year, week_numbers) {
          jQuery.each(week_numbers, function (week_number, weekdays) {
            year = parseInt(year);
            week_number = parseInt(week_number);
            if ((current_year === year && week_number <= current_week) ||
              (year === (current_year - 1) && week_number >= last_year_week)) {
              jQuery.each(weekdays, function (weekday, commits_done) {
                var month_name
                  = getMonthNameFromWeekNumber(year, week_number);
                var key = month_name + '\'' + year%100;
                if (isNaN(charts_data.commits[key])) {
                  charts_data.commits[key] = 0;
                }
                charts_data.commits[key] += Object.keys(commits_done).length;
              });
            }
          });
        });

        reviews_stats = repo_stats.reviews;
        jQuery.each(reviews_stats, function (year, week_numbers) {
          jQuery.each(week_numbers, function (week_number, weekdays) {
            year = parseInt(year);
            week_number = parseInt(week_number);
            if ((current_year === year && week_number <= current_week) ||
              (year === (current_year - 1) && week_number >= last_year_week)) {
              jQuery.each(weekdays, function (weekday, reviews_done) {
                var month_name = getMonthNameFromWeekNumber(year, week_number);
                var key = month_name + '\'' + year%100;
                if (isNaN(charts_data.reviews[key])) {
                  charts_data.reviews[key] = 0;
                }
                charts_data.reviews[key] += Object.keys(reviews_done).length;
              });
            }
          });
        });
      });
    }

    else {

      var last_twelve_weeks = get_last_twelve_weeks_begin_end();
      current_year = last_twelve_weeks[0];
      current_week = last_twelve_weeks[1];
      var last_twelfth_week = last_twelve_weeks[2];

      jQuery.each(hoster_stats, function (repo_name, repo_stats) {

        issue_stats = repo_stats.issues;
        jQuery.each(issue_stats, function (issue_type, years) {
          if (charts_data.issues[issue_type] === undefined) {
            charts_data.issues[issue_type] = new Map();
          }
          jQuery.each(years, function (year, week_numbers) {
            jQuery.each(week_numbers, function (week_number, weekdays) {
              if ((current_year === parseInt(year) &&
                    last_twelfth_week <= parseInt(week_number) &&
                    parseInt(week_number) <= current_week &&
                    current_week >= 12) ||
                  (parseInt(year) === (current_year - 1) &&
                    parseInt(week_number) >= last_twelfth_week &&
                    current_week < 12)) {
                jQuery.each(weekdays, function (weekday, issues) {
                  var key = 'Week-' + week_number + ',' + year;
                  if (isNaN(charts_data.issues[issue_type][key])) {
                    charts_data.issues[issue_type][key] = 0;
                  }
                  charts_data.issues[issue_type][key] +=
                    Object.keys(issues).length;
                });
              }
            });
          });
        });

        prs_stats = repo_stats.prs || repo_stats.merge_requests;
        jQuery.each(prs_stats, function (pr_type, years) {
          if (charts_data.merge_requests[pr_type] === undefined) {
            charts_data.merge_requests[pr_type] = new Map();
          }
          jQuery.each(years, function (year, week_numbers) {
            jQuery.each(week_numbers, function (week_number, weekdays) {
              if ((current_year === parseInt(year) &&
                    last_twelfth_week <= parseInt(week_number) &&
                    parseInt(week_number) <= current_week &&
                    current_week >= 12) ||
                (parseInt(year) === (current_year - 1) &&
                  parseInt(week_number) >= last_twelfth_week &&
                  current_week < 12)) {
                jQuery.each(weekdays, function (weekday, mrs) {
                  var key = 'Week-' + week_number + ',' + year;
                  if (isNaN(charts_data.merge_requests[pr_type][key])) {
                    charts_data.merge_requests[pr_type][key] = 0;
                  }
                  charts_data.merge_requests[pr_type][key] +=
                    Object.keys(mrs).length;
                });
              }
            });
          });
        });

        commits_stats = repo_stats.commits;
        jQuery.each(commits_stats, function (year, week_numbers) {
          jQuery.each(week_numbers, function (week_number, weekdays) {
            if ((current_year === parseInt(year) &&
                  last_twelfth_week <= parseInt(week_number) &&
                  parseInt(week_number) <= current_week &&
                  current_week >= 12) ||
                (parseInt(year) === (current_year - 1) &&
                  parseInt(week_number) >= last_twelfth_week &&
                  current_week < 12)) {
              jQuery.each(weekdays, function (weekday, commits_done) {
                var key = 'Week-' + week_number + ',' + year;
                if (isNaN(charts_data.commits[key])) {
                  charts_data.commits[key] = 0;
                }
                charts_data.commits[key] += Object.keys(commits_done).length;
              });
            }
          });
        });

        reviews_stats = repo_stats.reviews;
        jQuery.each(reviews_stats, function (year, week_numbers) {
          jQuery.each(week_numbers, function (week_number, weekdays) {
            if ((current_year === parseInt(year) &&
                  last_twelfth_week <= parseInt(week_number) &&
                  parseInt(week_number) <= current_week &&
                  current_week >= 12) ||
                (parseInt(year) === (current_year - 1) &&
                  parseInt(week_number) >= last_twelfth_week &&
                  current_week < 12)) {
              jQuery.each(weekdays, function (weekday, reviews_done) {
                var key = 'Week-' + week_number + ',' + year;
                if (isNaN(charts_data.reviews[key])) {
                  charts_data.reviews[key] = 0;
                }
                charts_data.reviews[key] += Object.keys(reviews_done).length;
              });
            }
          });
        });
      });
    }

    toggleCanvasDisplays(charts_data);
    setCanvasCharts(charts_data);
  }

  function addEventListenerToStatisticsSelector(contrib_data){
    hoster_selector.on('change', function () {
      updateCharts(contrib_data, hoster_selector.val(), stats_divider.val());
    });
    stats_divider.on('change', function () {
      updateCharts(contrib_data, hoster_selector.val(), stats_divider.val());
    });
    updateCharts(contrib_data, hoster_selector.val(), stats_divider.val());
  }

  function getContributionsCount(data){
    var contributions_count = 0;
    jQuery.each(data, function (years, contributions) {
      jQuery.each(contributions, function (weeknumbers, weekdays) {
        contributions_count += Object.keys(weekdays).length;
      });
    });
    return contributions_count;
  }

  function createRepositoryCanvasChart(data){
    var repositories_stats = {
      repositories: [], commits: [], reviews: [], issues_opened: [],
      assigned_issues: [], issues_closed: [], merge_requests_opened: [],
      unmerged_merge_requests: []
    };
    var github_data = data.statistics.github,
        gitlab_data = data.statistics.gitlab;
    jQuery.each(github_data, function (repository, stats) {
      repositories_stats.repositories.push(repository);
      repositories_stats.commits.push(getContributionsCount(stats.commits));
      repositories_stats.reviews.push(getContributionsCount(stats.reviews));
      repositories_stats.issues_opened.push(getContributionsCount(
        stats.issues === undefined? new Map(): stats.issues.open
      ));
      repositories_stats.assigned_issues.push(getContributionsCount(
        stats.issues === undefined? new Map(): stats.issues.assigned
      ));
      repositories_stats.issues_closed.push(getContributionsCount(
        stats.issues === undefined? new Map(): stats.issues.closed
      ));
      repositories_stats.merge_requests_opened.push(getContributionsCount(
        stats.prs === undefined? new Map(): stats.prs.open
      ));
      repositories_stats.unmerged_merge_requests.push(getContributionsCount(
        stats.prs === undefined? new Map(): stats.prs.unmerged
      ));
    });

    jQuery.each(gitlab_data, function (repository, stats) {
      repositories_stats.repositories.push(repository);
      repositories_stats.commits.push(getContributionsCount(stats.commits));
      repositories_stats.reviews.push(getContributionsCount(stats.reviews));
      repositories_stats.issues_opened.push(getContributionsCount(
        stats.issues === undefined? new Map(): stats.issues.opened
      ));
      repositories_stats.assigned_issues.push(getContributionsCount(
        stats.issues === undefined? new Map(): stats.issues.assigned
      ));
      repositories_stats.issues_closed.push(getContributionsCount(
        stats.issues === undefined? new Map(): stats.issues.closed
      ));
      repositories_stats.merge_requests_opened.push(getContributionsCount(
        stats.merge_requests === undefined? new Map():
          stats.merge_requests.opened
      ));
      repositories_stats.unmerged_merge_requests.push(getContributionsCount(
        stats.merge_requests === undefined? new Map():
          stats.merge_requests.unmerged
      ));
    });
    setRepositoryCanvasChart(repositories_stats);
  }

  $('select').formSelect();
  $('.user-statistics-option').on('click', function () {
    var username = $(this).attr('username');
    user_statistics_display.css('display', 'block');
    $.getJSON("/static/contributors-data.json", function (data) {
      var contrib_data = data[username];
      contrib_data.statistics = $.parseJSON(contrib_data.statistics);
      contrib_data.type_of_issues_worked_on = $.parseJSON(
        contrib_data.type_of_issues_worked_on
      );
      contrib_data.working_on_issues_count = $.parseJSON(
        contrib_data.working_on_issues_count
      );
      contrib_data.updated_at = $.parseJSON(contrib_data.updated_at);
      createRepositoryCanvasChart(contrib_data);
      addEventListenerToStatisticsSelector(contrib_data);
      displayWorkedOnIssueLabels(contrib_data);
      displayWorkingOnIssuesCount(contrib_data);
      displayDataUpdatedDates(contrib_data);
    }).fail(function (data, textStatus, error) {
      console.error("Request Failed: " + textStatus + ", " + error);
    });
    $('.close-statistics').on('click', function () {
      user_statistics_display.css('display', 'none');
    });
  });
});
