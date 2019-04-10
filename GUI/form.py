# Source: https://stackoverflow.com/questions/8560959/using-python-to-sign-into-website-fill-in-a-form-then-sign-out

import urllib, urllib.parse, urllib.request
import os, webbrowser

url = 'https://donjon.bin.sh/d20/dungeon/'
values = {'name' : 'The Undercrypt of Testing',
          'level' : '1',
          'motif' : 'none',
          'seed' : '1',
          'map_style' : 'Standard',
          'grid' : 'Square',
          'dungeon_layout' : 'Square',
          'dungeon_size' : 'Medium',
          'peripheral_egress' : 'No',
          'add_stairs' : 'No',
          'room_layout' : 'Dense',
          'room_size' : 'Medium',
          'door_set' : 'Standard',
          'corridor_layout' : 'Errant',
          'remove_deadends' : 'Some'}

values_bytes = urllib.parse.urlencode(values)
values_bytes = values_bytes.encode('utf-8')

data = urllib.parse.urlencode(values)
request = urllib.request.Request(url, values_bytes)
response = urllib.request.urlopen(request)
the_page = response.read()

# View generated page for testing purposes
path = os.path.abspath('temp.html')
url = 'file://' + path
with open(path, 'w') as f:
    f.write(the_page.decode('utf-8'))
webbrowser.open(url)
