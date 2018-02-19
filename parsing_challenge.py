import json, random
import dateparser
from dateparser.search import search_dates
import datetime
from geopy.geocoders import Nominatim
import re

geolocator = Nominatim()
pattern = r"(\d{4})-(\d{2})-(\d{2})"
with open('parsing_challenge.json') as json_data:
    data = json.load(json_data)
sample = random.randint(0, len(data))
answer_sample = []

#print(data[60720])
#print (search_dates("Maumee United States of America, 02/09/2016"))
dates_found = []
for i in range(10):
    answer_sample.append([sample+i,  data[sample+i], 'date', 'ranking', 'ranking-address', 'road', 'city', 'country'])
    #answer_sample.append([92640 + i, data[92640 + i], 'date', 'ranking-date', 'ranking-address', 'road', 'city', 'country'])
print (answer_sample)
for i in answer_sample:
    try:
        dates_found = search_dates(i[1])
    except ZeroDivisionError:
        i[1] = i[1].replace('of America', "FixedError")
        dates_found = search_dates(i[1])

    if dates_found is not None:
        i[2] = dates_found[0][1].strftime("%Y-%m-%d")
        rank = dateparser.date.DateDataParser().get_date_data(dates_found[0][0])
        i[3] = rank['period']
        i[1] = i[1].replace(dates_found[0][0],"")
    else:
        i[3] = "No date"
        tmp = re.search(pattern, i[1])
        if tmp is not None:
            i[3] = 'day'
            i[2] = '{}-{}-{}'.format(tmp.group(1),tmp.group(2),tmp.group(3))

    i[1] = i[1].replace("FixedError", 'of America')
    location = geolocator.geocode(i[1], addressdetails=True)
    if location is not None:
        counter = 0
        if 'road' in location.raw['address']:
            i[5] = location.raw['address']['road']
            counter += 1
        if 'city' in location.raw['address']:
            i[6] = location.raw['address']['city']
            counter += 1
        if 'country' in location.raw['address']:
            i[7] = location.raw['address']['country']
            counter += 1
        if counter==3:
            i[4] = "Full address"
        else:
            i[4] = "Part-known address"
    elif len(i[1])>1:
        i[4] = "Unknown address"
    else:
        i[4] = "No address"
    print(i)


