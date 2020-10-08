from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import WeeklyRepeatingTimer

class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None):
		self.year = year
		self.month = month
		super(Calendar, self).__init__()

	# formats a day as a td
	# filter events by day
	def formatday(self, day, weekday, events):
		#events_per_day = events.filter(start_time__day=day)
		events_per_day = []
		for event in events:
			for weekdayEvent in event.weekdays.all():
				if weekdayEvent.label == 'Montag' and weekday == 0:
					events_per_day.append(event)
				if weekdayEvent.label == 'Dienstag' and weekday == 1:
					events_per_day.append(event)
				if weekdayEvent.label == 'Mittwoch' and weekday == 2:
					events_per_day.append(event)
				if weekdayEvent.label == 'Donnerstag' and weekday == 3:
					events_per_day.append(event)
				if weekdayEvent.label == 'Freitag' and weekday == 4:
					events_per_day.append(event)
				if weekdayEvent.label == 'Samstag' and weekday == 5:
					events_per_day.append(event)
				if weekdayEvent.label == 'Sonntag' and weekday == 6:
					events_per_day.append(event)
		d = ''
		for event in events_per_day:
			formatedTimeStart = event.timestart.strftime("%H:%M")
			formatedTimeStop = event.timestop.strftime("%H:%M")
			d += f'<li> <a href="/settings/{event.id}_alter_timer"> {event.label} <br> {formatedTimeStart} - {formatedTimeStop} </a> </li>'

		if day != 0:
			return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
		return '<td></td>'

	# formats a week as a tr 
	def formatweek(self, theweek, events):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, weekday, events)
		return f'<tr> {week} </tr>'

	# formats a month as a table
	# filter events by year and month
	def formatmonth(self, withyear=True):
		events = WeeklyRepeatingTimer.objects.all()
		#.objects.filter(timestart__year=self.year, timestart__month=self.month)

		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, events)}\n'
		return cal