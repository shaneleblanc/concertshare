import requests
import json
import os
from datetime import datetime

spotify_client = '88ab7ee1188f4ec7b08e408a274f087f'
spotify_secret = 'a67c6bbf01884fcc932f68097c62a542'
app_id = 'cce6519e13b087ac855b87610aeec854'

def get_spotify_artists():
    return
    # Requres user authorization
    # TODO: Confirm URL for site so we have a callback URL for authorization requests
    # TODO: Authorize a user with their spotify account, then pull their followed artists
    # TODO: Last.fm Get Artists is the same process, authorization with callback -> get top artists

def get_artist_info(artist):
    response = requests.get(f'https://rest.bandsintown.com/artists/{artist}?app_id={app_id}')
    data = json.loads(response.content)
    print(data.keys())
    upcoming_count = data['upcoming_event_count']
    id = data['id']
    url = data['url']
    thumb_url = data['thumb_url']
    image_url = data['image_url']
    facebook_page_url = data['facebook_page_url']

get_artist_info('Coldplay')

def get_event_info(artist, date_range):
    date_range.replace(',', '%2C')
    # Dates must be foormatted as YYYY-MM-DD,YYYY-MM-DD - the comma must turn into a '%2C' in the URL
    response = requests.get(f'https://rest.bandsintown.com/artists/{artist}/events?app_id={app_id}&date={date_range}')
    data = json.loads(response.content)
    # tableING HTML DISPLAY EVENT INFO BELOW
    table_html = '<table class="table table-dark">\n<thead>\n<tr>\n<th scope="col">#</th>'
    event_keys = ['Line-up', 'Venue', 'Date', 'On sale', 'Tickets']

    for item in event_keys: # Top row
        table_html += f'<th scope="col">{item}</th>'
    table_html += '</tr>\n</thead>\n<tbody>'
    event_num = 1
    for item in data[1:]: # Data rows
        table_html += f'''<tr><th scope="row">{event_num}</th>
        <td>{', '.join(item['lineup'])}</td>
        <td>{item['venue']['name']} in {item['venue']['city']}, {item['venue']['country']} ({item['venue']['region']})</td>
        <td>{item['datetime']}</td>
        <td>{item['on_sale_datetime']}</td>
        <td><a href="{item['url']}">Get tickets</a></td>
        </tr>
        '''
        event_num += 1
    print(data[0].keys())
    table_file = open('tabletemplate.html').read()
    table_file = table_file.replace('{content}', table_html)
    open('table.html', 'w').write(table_file)
    # END tableING CODE
    return(data)

print(get_event_info('Drake', '2018-06-01,2019-08-01'))
