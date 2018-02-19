import json, random
import pandas as pd
import dateparser
from dateparser.search import search_dates
import datetime
from geopy.geocoders import Nominatim

geolocator = Nominatim()
with open('parsing_challenge.json') as json_data:
    data = json.load(json_data)
sample = random.randint(0, len(data))
answer_sample = []
#print(data[60720])
#print (search_dates("Maumee United States of America, 02/09/2016"))
dates_found = []
for i in range(10):
    answer_sample.append([sample+i,  data[sample+i], 'date', 'ranking'])
    #answer_sample.append([4468 + i, data[33 + i], 'date'])
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
    i[1] = i[1].replace("FixedError", 'of America')
    location = geolocator.geocode(i[1], addressdetails=True)
    if location is not None:
        if 'city' in location.raw['address']:
            print (location.raw['address']['city'])
        if 'country' in location.raw['address']:
            print(location.raw['address']['country'])
        if 'road' in location.raw['address']:
            print(location.raw['address']['road'])
    print(i)


