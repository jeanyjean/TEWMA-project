"""Utility file for Calendar class."""
from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Meeting
# from eventcalendar.helper import get_current_user


class Calendar(HTMLCalendar):
    """ """

    def __init__(self, year=None, month=None):
        """Initialize Calendar class."""
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    def formatday(self, day, meetings):
        """Return table HTML tag with list of meeting."""
        meets_per_day = meetings.filter(start_time__day=day)
        meets_in_day = ''
        for meet in meets_per_day:
            meets_in_day += f"<li> {meet.subject} </li>"
        if day != 0:
            return f"<td><a href='#'><span class='date'>{day}</span></a><ul> {meets_in_day} </ul></td>"
        return '<td><a></a></td>'

    def formatweek(self, theweek, meetings):
        """Return table row HTML tag for each week."""
        week = ''
        for day, weekday in theweek:
            week += self.formatday(day, meetings)
        return f"<tr><a> {week} </a></tr>"

    def formatmonth(self, withyear=True):
        """Return a one month of calendar."""
        meetings = Meeting.objects.filter(start_time__year=self.year, start_time__month=self.month)
        calendar = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        calendar += f'{self.formatmonthname(self.year, self.month, withyear= withyear)}\n'
        calendar += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            calendar += f'{self.formatweek(week, meetings)}\n'
        return calendar
