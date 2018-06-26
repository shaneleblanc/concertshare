from django.shortcuts import render
import requests
import json
from datetime import datetime
import arrow

app_id = 'cce6519e13b087ac855b87610aeec854'
# Create your views here.
def homepage(request):
    return render(request, 'pages/home.html', {})

def event_list(request, artist, date_range):
    response = requests.get(f'https://rest.bandsintown.com/artists/{artist}/events?app_id={app_id}&date={date_range}')
    data = json.loads(response.content)

    event_keys = ['Line-up', 'Venue', 'Date', 'On sale', 'Tickets']
    events = []
    event_num = 1

    for item in data[1:]: # Data rows
        event_date = arrow.get(item['datetime']).format('MMMM D, h a')
        if(item['on_sale_datetime'] != ''):
            on_sale_date = arrow.get(item['on_sale_datetime']).humanize()
        else:
            on_sale_date = ''
        event = {
            'number': event_num,
            'lineup': ', '.join(item['lineup']),
            'venue': item['venue'],
            'datetime': event_date,
            'on_sale_datetime': on_sale_date,
            'url': item['url'],
        }

        events.append(event)
        event_num += 1

    context = {
        'event_keys': event_keys,
        'events': events,
    }

    return render(request, 'pages/events.html', context)
