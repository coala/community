import requests
import json
import datetime
import os
import calendar
from dateutil import parser, relativedelta


class Scraper():
    """
    This is the class responsible for scraping provided issues into a
    dictionary containing just statistical information of the data.
    """

    """
    Count of months/weeks/days respectively to be scraped in past.
    """
    CONSTANTS = {
        'month_count': 12,
        'week_count': 4,
        'day_count': 7,
    }

    def __init__(self, content, date):
        """
        Constructs a new ``Scraper``

        :param content: Github API Parsed JSON issues
        :param date: The date to scrape data till.
        """
        self.date = date
        self.content = content

        # Initialise data dicts
        self.data = {
            'year': {
                'labels': [],
                'closed': [0]*self.CONSTANTS['month_count'],
                'opened': [0]*self.CONSTANTS['month_count'],
            },
            'month': {
                'labels': [],
                'closed': [0]*self.CONSTANTS['week_count'],
                'opened': [0]*self.CONSTANTS['week_count'],
            },
            'week': {
                'labels': [],
                'closed': [0]*self.CONSTANTS['day_count'],
                'opened': [0]*self.CONSTANTS['day_count'],
            },
        }

        # Process labels for each option
        for x in range(self.CONSTANTS['month_count']-1, -1, -1):
            self.data['year']['labels'].append(calendar.month_name[(
                self.date - relativedelta.relativedelta(months=x)).month])

        for x in range(self.CONSTANTS['week_count']-1, -1, -1):
            day = self.date - relativedelta.relativedelta(weeks=x)
            strt = (day - datetime.timedelta(days=day.weekday()))
            fin = (day + datetime.timedelta(days=6-day.weekday()))
            self.data['month']['labels'].append(
                calendar.month_abbr[strt.month] + ' ' + str(strt.day)
                + ' - '
                + calendar.month_abbr[fin.month] + ' ' + str(fin.day))

        for x in range(self.CONSTANTS['day_count']-1, -1, -1):
            day_idx = (self.date - datetime.timedelta(days=x)).weekday()
            self.data['week']['labels'].append(calendar.day_name[day_idx])

    def __diff_month(self, d):
        """
        :param d: Date as datetime, self.date >= Date.

        :return: Difference in months(int) ignoring partially complete months.
        """
        return (self.date.year - d.year) * 12 + self.date.month - d.month

    def __diff_week(self, d):
        """
        :param d: Date as datetime, self.date >= Date.

        :return: Difference in weeks(int) ignoring partially complete weeks.
        """
        monday1 = (self.date - datetime.timedelta(days=self.date.weekday()))
        monday2 = (d - datetime.timedelta(days=d.weekday()))
        return (monday1 - monday2).days // 7

    def __diff_days(self, d):
        """
        :param d: Date as datetime, self.date >= Date.

        :return: Difference in days(int) ignoring partially complete days.
        """
        return (self.date-d).days

    def get_data(self):
        """
        Get data

        :return: Data in form of dict containing year, month, week data.
        """
        for issue in self.content:
            issue = issue['issue']
            # Parse date, while ignoring the timestamp.
            dt = parser.parse(issue['createdAt'][:10])

            mon = self.__diff_month(dt)
            if mon < self.CONSTANTS['month_count']:
                mon = self.CONSTANTS['month_count'] - mon - 1
                self.data['year']['opened'][mon] += 1
                if issue['state'] == 'closed':
                    self.data['year']['closed'][mon] += 1

            wk = self.__diff_week(dt)
            if wk < self.CONSTANTS['week_count']:
                wk = self.CONSTANTS['week_count'] - wk - 1
                self.data['month']['opened'][wk] += 1
                if issue['state'] == 'closed':
                    self.data['month']['closed'][wk] += 1

            dys = self.__diff_days(dt)
            if dys < self.CONSTANTS['day_count']:
                dys = self.CONSTANTS['day_count'] - dys - 1
                self.data['week']['opened'][dys] += 1
                if issue['state'] == 'closed':
                    self.data['week']['closed'][dys] += 1

        return self.data


if __name__ == '__main__':

    org_name = open('org_name.txt').readline()

    # URL to grab all issues from
    issues_url = 'http://' + org_name + '.github.io/gh-board/issues.json'

    content = requests.get(issues_url)
    content.raise_for_status()
    parsed_json = content.json()

    real_data = Scraper(parsed_json['issues'], datetime.datetime.today())
    real_data = real_data.get_data()

    print(real_data)
    with open('static' + os.sep + 'activity-data.json', 'w') as fp:
        json.dump(real_data, fp)
