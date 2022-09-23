# Usage: python extract_match_data.py <URL>
# Example:
# python extract_match_data.py "https://sporza.be/nl/matches/voetbal/eur/europees-kampioenschap/2020/1-8-finale/01/frankrijk-zwitserland-livestream-verrassing-seferovic-kopt-zwitserland-op-voorsprong~1575469020455/"
import sys
from urllib.request import urlopen
import json

from wk2022.models import Player


def extract_match_data(url):
    # Open url and read data into string
    data = urlopen(url).read()
    body = data.decode('utf-8')
    # Split string into list of lines
    body_lines = body.split('\n')
    # Search for the line containing the page data, and check that there is just one line. Use list comprehension
    info_line = [item for item in body_lines if ('data-hypernova-key="Scoreboard"' in item and 'reqUrl' in item)]
    assert len(info_line) == 1
    # Convert 1-element list to string
    info_line = info_line[0]
    # Poor man's way of searching for start and end statement of json
    index_string_start = info_line.find('<!--')
    index_string_end = info_line.find('-->')
    # Parse json
    json_string = info_line[index_string_start + 4: index_string_end]
    match_data = json.loads(json_string)
    # Return the dictionary
    return match_data


def readscreen():
    url = "https://sporza.be/wedstrijd/~3261955"
    match_data = extract_match_data(url)
    print('Home squad')
    print('----------')
    allplayers = Player.objects.all()
    for home_player in match_data['data']['homeSquad']['lineup']:
        print(home_player['player']['name'])
        for speler in allplayers:
            if (speler.first_name in home_player['player']['name']) & (speler.last_name in home_player['player']['name']):
                print(home_player['player']['name'] + " exists")
    print('')
    print('Away squad')
    print('----------')
    for away_player in match_data['data']['awaySquad']['lineup']:
        for speler in allplayers:
            if (speler.first_name in away_player['player']['name']) & (speler.last_name in away_player['player']['name']):
                print(away_player['player']['name'] + " exists")
    return match_data
