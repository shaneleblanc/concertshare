from django.shortcuts import render
import requests
import json
from datetime import datetime
import arrow
from concertshare.users.models import User
from concertshare.users.models import Group

app_id = 'cce6519e13b087ac855b87610aeec854'
# Create your views here.
def homepage(request):
    return render(request, 'pages/home.html', {})

def create_group(request):
    the_user = User.objects.get(username=request.user.username)
    gname = f"{the_user}\'s group"
    new_group = Group.objects.create(name=gname)
    add_user_to_group(the_user)
    context = {
        'group': new_group,
    }
    message = "New group created!"
    return group_list(request, message)

def add_user_to_group(the_user):
    new_group.users.add(the_user)
    new_group.artists += the_user.artists
    new_group.cities += the_user.cities
    new_group.date_range = the_user.date_range # this is temporary!
    new_group.save()

def group_list(request, message=''):
    the_user = User.objects.get(username=request.user.username)
    users_groups = [i for i in Group.objects.all().filter(users=the_user)]
    count = 1
    for item in users_groups:
        item.number = count
        count += 1

    context = {
        'groups': users_groups,
        'message': message
    }
    return render(request, 'pages/group_list.html', context)

def event_list(request):
    the_user = User.objects.get(username=request.user.username)
    date_range = the_user.date_range
    event_keys = ['Line-up', 'Venue', 'Date', 'On sale', 'Tickets']
    events = []
    event_num = 1
    artists = the_user.artists.split(', ')
    for artist in artists:
        print(artist)
        try:
            response = requests.get(f'https://rest.bandsintown.com/artists/{artist}/events?app_id={app_id}&date={date_range}')
            data = json.loads(response.content)
        except json.decoder.JSONDecodeError:
            print("That's a JSON Decode error boys and girls")
            data = {}

        if(data != {}):
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
