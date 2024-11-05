import sys
import argparse
import datetime
from icalendar import Calendar, Event, Alarm
import holidays

parser = argparse.ArgumentParser(description='Generate Camping Booking Dates and Optional Calendar File')
parser.add_argument('-s', '--start', help='Start Date (MM/DD/YYYY)', required=True)
parser.add_argument('-e', '--end', help='End Date (MM/DD/YYYY)', required=True)
parser.add_argument('-c', '--calendar', help='Generate Calendar File (Optional)', action='store_true')

months_num = {'1': 31, '2': 28, '3': 31, '4': 30, '5': 31, '6': 30, '7': 31, '8': 31, '9': 30, '10': 31, '11': 30, '12': 31}

us_holidays = holidays.US(state='CA')

reminder1 = 24
reminder2 = 4

def get_6_months_back(date):
    year = date.year
    month = date.month
    day = date.day

    if month <= 6:
        month += 6
        year -= 1
    else:
        month -= 6
    
    # Assumes basic leap year rules
    if month == 2 and year % 4 == 0:
        if day > 29:
            day = 1
            month = 3

    if day > months_num[str(month)]:
        day = 1
        if month == 12:
            month = 1
            year += 1
        else:
            month += 1
    
    return datetime.date(year, month, day)

def monday_holiday(date):
    days_until_monday = (7 - date.weekday()) % 7
    next_monday = date + datetime.timedelta(days_until_monday)
    if next_monday in us_holidays:
        return True, us_holidays[next_monday]
    return False, None

def parse_error(msg):
    print(msg)
    parser.print_help()
    sys.exit(1)

def parse_date(date):
    try:
        month, day, year = date.split('/')
        month = int(month)
        day = int(day)
        year = int(year)
        if month < 1 or month > 12:
            parse_error('Invalid month')
        if day < 1 or day > months_num[str(month)]:
            parse_error('Invalid day')
        return datetime.date(year, month, day)
    except ValueError:
        parse_error('Invalid date format')
    return None

def main():
    args = parser.parse_args()
    start_date = parse_date(args.start)
    end_date = parse_date(args.end)
    date_array = []

    itr = start_date if start_date.weekday() == 4 else start_date + datetime.timedelta((4 - start_date.weekday()) % 7)
    while itr <= end_date:
        back_date = get_6_months_back(itr)
        
        is_holiday, holiday = monday_holiday(itr)
        holiday_str = (' - ' + holiday + ' weekend') if is_holiday else ''

        title = 'Camping Booking - ' + itr.strftime('%m/%d/%Y') + holiday_str.upper()

        print(title, '-- Book on', back_date.strftime('%m/%d/%Y'))
        date_array.append((back_date, itr, title))
        itr += datetime.timedelta(7)

    if args.calendar:
        calendar = Calendar()

        for back_date, book_date, title in date_array:
            event = Event()
            event.add('summary', title)
            event.add('dtstart', back_date)
            event.add('dtend', back_date + datetime.timedelta(1))
            event.add('description', 'Date to Book Camping for ' + book_date.strftime('%m/%d/%Y'))
            event.add('location', 'Online')
            event.add('transp', 'TRANSPARENT')

            alarm_disp_1 = Alarm()
            alarm_disp_1.add('action', 'display')
            alarm_disp_1.add('description', str(reminder1) + ' Hour Reminder: ' + title)
            alarm_disp_1.add('trigger', datetime.timedelta(hours=-reminder1))

            alarm_disp_2 = Alarm()
            alarm_disp_2.add('action', 'display')
            alarm_disp_2.add('description', str(reminder2) + ' Hour Reminder: ' + title)
            alarm_disp_2.add('trigger', datetime.timedelta(hours=-reminder2))

            event.add_component(alarm_disp_1)
            event.add_component(alarm_disp_2)

            calendar.add_component(event)
        
        with open('camping_booking.ics', 'wb') as f:
            f.write(calendar.to_ical())
        
        print('Calendar file generated: camping_booking.ics')
        print('Import into your calendar application')
        print('Recommended to Create a New Calendar for these reminders, to not clutter your main calendar')

if __name__ == '__main__':
    main()