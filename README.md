# Booking Calendar Generator for California Camping

Generates the Dates and an ICS Calendar for Booking Dates for California State Park Campgrounds

Configured for Weekend bookings, Outputs the dates so you can book for Fridays. Holiday weekends are noted based on Monday holidays. 

Also generates reminders for supported calendar clients

### Required Dependencies

Requires Python 3 as well as `argparse, icalendar, holidays` - install using `pip install argparse icalendar holidays`

### Execution

Run the script and get help message using `python3 script.py -h`

Follow subsequent directions to execute as needed

If you would like to change the alarm period, change the `reminder` variables at the file header

Note: Google Calendar does not Support reminders - you can add these entries to a new calendar and then set the calendar to have notifications globally