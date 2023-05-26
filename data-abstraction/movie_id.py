import urllib.request
import requests
import datetime
import time
from keys import key

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
    "Accept": "application/json"
}


def get_movie_ids():
    URL = "https://api.themoviedb.org/3/discover/movie/"

    # Initialize date to beging fetching movies from
    year = 2000
    month = 1
    day = 1

    # Loop through all months following January 1, 1940 until February 1, 2023
    while (datetime.date(year, month, day).strftime("%Y/%m/%d") != '2023/02/01'):

        # Array to store movie ids
        movie_ids = []

        # Loop through all months following January 1, 1940 until February 1, 2023.
        # To start, we grab movie ids from Jan 1, 1940 to Feb 1, 1940. Following,
        # we search from the 2nd of the month, to the 1st of the following month.
        if (datetime.date(year, month, day).strftime("%Y/%m/%d") == '1940/01/01'):
            start_date = datetime.date(year, month, day)
        else:
            start_date = datetime.date(year, month, day+1)

        # Increment the month by 1 to be used in end_date variable.
        # If the current month is december set the next month to 1.
        if month == 12:
            year = year + 1
            month = 1
        else:
            month = month + 1

        end_date = datetime.date(year, month, day)

        print("start date: " + start_date.strftime("%Y/%m/%d"))
        print("end date: " + end_date.strftime("%Y/%m/%d"))

        # Set params for API search
        PARAMS = {'api_key': key,
                  'primary_release_date.gte': start_date,
                  'primary_release_date.lte': end_date}

        # Get API data
        try:
            r = requests.get(url=URL, params=PARAMS, headers=header)
        except:
            print('Initial request error... Waiting one minute...\n')
            time.sleep(60)
            r = requests.get(url=URL, params=PARAMS, headers=header)

        try:
            data = r.json()
        except:
            print('Data error... Waiting one minute...\n')
            data = r.json()

        # Get total number of pages
        pages = data['total_pages']

        # Get results for page 1
        results = len(data['results'])

        # Append each movie id from page 1 to the array
        for movie in range(results):
            movie_ids.append(data['results'][movie]['id'])

        # Add each movie id from every possible page to the array
        for x in range(1, pages):
            PARAMS.update({'page': x + 1})
            try:
                r = requests.get(url=URL, params=PARAMS, headers=header)
            except:
                print('Request error for ' + start_date.strftime("%Y/%m/%d") + ' to ' + end_date.strftime(
                    "%Y/%m/%d") + ' specifically on page: ' + str(x+1) + '... Waiting one minute...\n')
                time.sleep(60)
                r = requests.get(url=URL, params=PARAMS, headers=header)
            data = r.json()
            results = len(data['results'])
            for movie in range(results):
                movie_ids.append(data['results'][movie]['id'])

            # Write all movie ids to csv file
        with open('C:\\Users\\shaki\\Documents\\GitHub\\movie-revenue-analysis\\data\\movie_ids.csv', 'a') as fp:
            for item in movie_ids:
                # write each item on a new line
                fp.write("%s\n" % item)
            print('Done!')
            print("===============================\n===============================")


get_movie_ids()
