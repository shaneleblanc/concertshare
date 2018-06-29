from django.shortcuts import render
import requests
import json
from datetime import datetime
import arrow
from concertshare.users.models import User

app_id = 'cce6519e13b087ac855b87610aeec854'
# Create your views here. 
def homepage(request):
    return render(request, 'pages/home.html', {})

def event_list(request):
    the_user = User.objects.get(username=request.user.username)
    date_range = the_user.date_range
    event_keys = ['Line-up', 'Venue', 'Date', 'On sale', 'Tickets']
    events = []
    event_num = 1
    for artist in the_user.artists.split(','):
        print(artist)
        response = requests.get(f'https://rest.bandsintown.com/artists/{artist}/events?app_id={app_id}&date={date_range}')
        data = json.loads(response.content)

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
            if item['venue']['city'] in the_user.cities:
                events.append(event)
                event_num += 1
                print("found show in user's city")



    context = {
        'event_keys': event_keys,
        'events': events,
    }

    return render(request, 'pages/events.html', context)
