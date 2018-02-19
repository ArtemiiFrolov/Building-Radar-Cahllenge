import json, random, sys
import dateparser
from dateparser.search import search_dates
import datetime
from geopy.geocoders import Nominatim
import re
import matplotlib.pyplot as plt

# lists, dictionaries and stuff
geolocator = Nominatim(timeout=10)
pattern_1 = r"(\d{4})-(\d{2})-(\d{2})"
pattern_2 = r"(\d{2})/(\d{2})/(\d{4})"
ranking_counter = {'day':0, 'month': 0, 'year': 0, 'nd': 0, 'na': 0, 'fa':0, 'pa':0, 'ua': 0}
answer_sample = []
dates_found = []


def main(argv):
    # opening file
    with open('parsing_challenge.json') as json_data:
        data = json.load(json_data)
    if len(argv)>1:
        # if we want to parse part of data
        for i in range(int(argv[0]), int(argv[1])):
            answer_sample.append(
                {'N': i, 'address': data[i], 'date': '', 'ranking': '', 'ranking-address': '',
                 'road': '', 'city': '', 'country': ''})
    else:
        # if we want to parse all data
        for i in range(len(data)):
            answer_sample.append(
                {'N': i, 'address': data[i], 'date': '', 'ranking': '', 'ranking-address': '',
                 'road': '', 'city': '', 'country': ''})
    for i in answer_sample:
        # finding date in every row of answer_sample and rank it
        i = find_date(i)
        # finding address in every row of answer_sample and rank it
        i = find_address(i)
        print(i)
    # graphics based on rankings
    analysis_1()
    analysis_2()
    # creating new file with edited data
    with open('data.json', 'w') as outfile:
        json.dump(answer_sample, outfile)
    pass


def find_date(one_value):
    # fixing one of error in library (when there is "am", library finds an error)
    one_value['address'] = one_value['address'].replace('am', "FixedError")
    one_value['address'] = one_value['address'].replace('Am', "FixedError")
    try:
        # trying to find data in row
        dates_found = search_dates(one_value['address'])
    except ZeroDivisionError:
        dates_found = None
    if dates_found is not None:
        # if we find any date - completing date row  and rank
        one_value['date'] = dates_found[-1][1].strftime("%Y-%m-%d")
        rank = dateparser.date.DateDataParser().get_date_data(dates_found[-1][0])
        one_value['ranking'] = rank['period']
        ranking_counter[rank['period']] += 1
        # cut date from orgignal string to have only address
        one_value['address'] = one_value['address'].replace(dates_found[-1][0], "")
    else:
        # if we don't find any date - completing rankings
        one_value['ranking'] = "no date"
        ranking_counter['nd'] += 1
        # checking exception of library - it doesnt find date in this format "2004-12-31T00:00:00Z"
        tmp = re.search(pattern_1, one_value['address'])
        if tmp is not None:
            # if he have date in given format - completing date row and rank
            one_value['ranking'] = 'day'
            one_value['date'] = '{}-{}-{}'.format(tmp.group(1), tmp.group(2), tmp.group(3))
            ranking_counter['day'] += 1
            ranking_counter['nd'] -= 1
        # checking exception of library - it doesnt find date in this format "mm/dd/yyyy"
        tmp = re.search(pattern_2, one_value['address'])
        if tmp is not None:
            # if he have date in given format - completing date row and rank
            one_value['ranking'] = 'day'
            one_value['date'] = '{}-{}-{}'.format(tmp.group(3), tmp.group(1), tmp.group(2))
            ranking_counter['day'] += 1
            ranking_counter['nd'] -= 1
    return one_value


def find_address(one_value):
    # replacing back "am" that was deleted to prevent library failure
    one_value['address'] = one_value['address'].replace("FixedError", 'am')
    if len(one_value['address']) > 1:
        # trying to find location of address
        try:
            location = geolocator.geocode(one_value['address'], addressdetails=True, language='en')
        except:
            location = None
        if location is not None:
            # if we found any location - trying to check road, city and country and completing rankings
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
                # if we have all information - complete rank as full address
                one_value['ranking-address'] = "full address"
                ranking_counter['fa'] += 1
            else:
                # if we don't  have all information - complete rank as part-known address
                one_value['ranking-address'] = "part-known address"
                ranking_counter['pa'] += 1
        else:
            # if we don't find any address, but have information, complete rank as unknown address
            one_value['ranking-address'] = "unknown address"
            ranking_counter['ua'] += 1
    else:
        # if we there is any information,  complete rank as no address
        one_value['ranking-address'] = "no address"
        ranking_counter['na'] += 1
    return one_value


def analysis_1():
    # pie-graphs that shows distribution of date rankings
    labels = 'day', 'month', 'year', 'no date'
    sizes = [ranking_counter['day'], ranking_counter['month'], ranking_counter['year'], ranking_counter['nd']]
    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
    explode = (0.1, 0, 0, 0)
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    plt.show()
    pass


def analysis_2():
    # pie-graphs that shows distribution of address rankings
    labels = 'full address', 'part-known address', 'unknown address', 'no address'
    sizes = [ranking_counter['fa'], ranking_counter['pa'], ranking_counter['ua'], ranking_counter['na']]
    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
    explode = (0.1, 0, 0, 0)
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    plt.show()
    pass

if __name__ == "__main__":
   main(sys.argv[1:])

