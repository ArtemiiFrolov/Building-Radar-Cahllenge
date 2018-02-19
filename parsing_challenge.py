import json, random
import dateparser
from dateparser.search import search_dates
import datetime
from geopy.geocoders import Nominatim
import re

geolocator = Nominatim()
pattern = r"(\d{4})-(\d{2})-(\d{2})"

def main(args):
    with open('parsing_challenge.json') as json_data:
        data = json.load(json_data)
    sample = random.randint(0, len(data))
    answer_sample = []
    dates_found = []
    for i in range(10):
        answer_sample.append(
            {'N': sample + i, 'address': data[sample + i], 'date': '', 'ranking': '', 'ranking-address': '',
             'road': '', 'city': '', 'country': ''})

    for i in answer_sample:
        i = find_date(i)
        i = find_address(i)
        print(i)
    return 2


def find_date(one_value):
    try:
        dates_found = search_dates(one_value['address'])
    except ZeroDivisionError:
        one_value['address'] = one_value['address'].replace('of America', "FixedError")
        dates_found = search_dates(one_value['address'])

    if dates_found is not None:
        one_value['date'] = dates_found[0][1].strftime("%Y-%m-%d")
        rank = dateparser.date.DateDataParser().get_date_data(dates_found[0][0])
        one_value['ranking'] = rank['period']
        one_value['address'] = one_value['address'].replace(dates_found[0][0], "")
    else:
        one_value['ranking'] = "No date"
        tmp = re.search(pattern, one_value['address'])
        if tmp is not None:
            one_value['ranking'] = 'day'
            one_value['date'] = '{}-{}-{}'.format(tmp.group(1), tmp.group(2), tmp.group(3))
    return one_value


def find_address(one_value):
    one_value['address'] = one_value['address'].replace("FixedError", 'of America')
    location = geolocator.geocode(one_value['address'], addressdetails=True, language='en')
    if location is not None:
        counter = 0
        if 'road' in location.raw['address']:
            one_value['road'] = location.raw['address']['road']
            counter += 1
        if 'city' in location.raw['address']:
            one_value['city'] = location.raw['address']['city']
            counter += 1
        if 'country' in location.raw['address']:
            one_value['country'] = location.raw['address']['country']
            counter += 1
        if counter == 3:
            one_value['ranking-address'] = "Full address"
        else:
            one_value['ranking-address'] = "Part-known address"
    elif len(one_value['address']) > 1:
        one_value['ranking-address'] = "Unknown address"
    else:
        one_value['ranking-address'] = "No address"
    return one_value

def analysis(one_list):
    
a = main(1)
