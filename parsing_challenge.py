import json, random
import dateparser
from dateparser.search import search_dates
import datetime
from geopy.geocoders import Nominatim
import re
import plotly
import plotly.plotly as py
import plotly.graph_objs as go

geolocator = Nominatim()
pattern = r"(\d{4})-(\d{2})-(\d{2})"
ranking_counter = {'day':0, 'month': 0, 'year': 0, 'nd': 0, 'na': 0, 'fa':0, 'pa':0, 'ua': 0}
plotly.tools.set_credentials_file(username='BadaBoooM63', api_key='tR8jFuFSijP46x4zNawh')

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
    analysis()
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
        ranking_counter[rank['period']] += 1
        one_value['address'] = one_value['address'].replace(dates_found[0][0], "")
    else:
        one_value['ranking'] = "no date"
        ranking_counter['nd'] += 1
        tmp = re.search(pattern, one_value['address'])
        if tmp is not None:
            one_value['ranking'] = 'day'
            one_value['date'] = '{}-{}-{}'.format(tmp.group(1), tmp.group(2), tmp.group(3))
            ranking_counter['day'] += 1
            ranking_counter['nd'] -= 1
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
            one_value['ranking-address'] = "full address"
            ranking_counter['fa'] += 1
        else:
            one_value['ranking-address'] = "part-known address"
            ranking_counter['pa'] += 1
    elif len(one_value['address']) > 1:
        one_value['ranking-address'] = "unknown address"
        ranking_counter['ua'] += 1
    else:
        one_value['ranking-address'] = "no address"
        ranking_counter['na'] += 1
    return one_value

def analysis():
    labels = ['day', 'month', 'year', 'no date']
    values = [ranking_counter['day'], ranking_counter['month'], ranking_counter['year'], ranking_counter['nd']]
    trace = go.Pie(labels=labels, values=values)
    py.iplot([trace], filename='basic_pie_chart')
    pass

a = main(1)
print(ranking_counter)
