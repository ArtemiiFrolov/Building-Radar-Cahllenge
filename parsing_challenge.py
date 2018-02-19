import json, random
import pandas as pd
import dateparser
from dateparser.search import search_dates
import datetime

with open('parsing_challenge.json') as json_data:
    data = json.load(json_data)
sample = random.randint(0, len(data))
answer_sample = []
#print(data[60720])
#print (search_dates("Maumee United States of America, 02/09/2016"))
dates_found = []
for i in range(10):
    answer_sample.append([sample+i,  data[sample+i], 'date'])
    #answer_sample.append([4468 + i, data[33 + i], 'date'])
for i in answer_sample:
    try:
        dates_found = search_dates(i[1])
        if dates_found is not None:
            i[2] = dates_found[0][1].strftime("%Y-%m-%d")
        print(i)
    except ZeroDivisionError:
        i[1] = i[1].replace('of America', "FixedError")
        dates_found = search_dates(i[1])
        if dates_found is not None:
            i[2] = dates_found[0][1].strftime("%Y-%m-%d")
        print(i)



