import requests
import datetime
import csv
from bs4 import BeautifulSoup


key = "d1a4982a7803d64c3582894a44ee43e9"


def movie_data():
    with open('actor_revenue.csv', mode='r', encoding="utf-8") as infile:
        reader = csv.reader(infile)
        actor_data = {rows[0]: rows[1] for rows in reader}

    with open('producer_revenue.csv', mode='r', encoding="utf-8") as infile:
        reader = csv.reader(infile)
        producer_data = {rows[0]: rows[1] for rows in reader}

    with open('director_revenue.csv', mode='r', encoding="utf-8") as infile:
        reader = csv.reader(infile)
        director_data = {rows[0]: rows[1] for rows in reader}

    with open('movie_data.csv', 'w', encoding="utf-8", newline='') as csvfile:

        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Id', 'Title', 'Action', 'Adventure', 'Animation',
                            'Comedy', 'Crime', 'Documentary', 'Drama', 'Family',
                            'Fantasy', 'Fantasy', 'History', 'Horror', 'Music',
                            'Mystery', 'Romance', 'Science Fiction', 'TV Movie',
                            'Thriller', 'War', 'Western', 'Original_Language',
                            'Average Production Company Earnings', 'Average Director Earnings',
                            'Average Producer Earnings', 'Average Actor Earnings',
                            'Budget', 'Revenue', 'Runtime', 'Adult'])

        URL = "https://api.themoviedb.org/3/movie/"

        file = open('test.txt', 'r')

        for i in range(100):
            URL = "https://api.themoviedb.org/3/movie/"

            movie_id = file.readline().strip()

            if not movie_id:
                break

            print(movie_id)
            URL = URL + movie_id
            PARAMS = {'api_key': key}
            passed = True
            try:
                r = requests.get(url=URL, params=PARAMS)
            except requests.exceptions.RequestException as e:
                passed = False

            if (passed):
                movie = r.json()
                movie_genres = []
                for genre in range(len(movie['genres'])):
                    movie_genres.append(movie['genres'][genre]['name'])

                URL = URL + '/credits'
                r = requests.get(url=URL, params=PARAMS)
                creds = r.json()

                cast = creds['cast']
                crew = creds['crew']

                average_actor_earnings = 0
                actors = 0
                for member in cast:
                    name = member['name']
                    if '(uncredited)' not in member['character']:

                        if name in actor_data:
                            average_actor_earnings = average_actor_earnings + \
                                int(actor_data[name])
                            actors = actors + 1
                        else:
                            actors = actors + 1
                if (actors != 0):
                    average_actor_earnings = average_actor_earnings / actors

                average_director_earnings = 0
                directors = 0
                average_producer_earnings = 0
                producers = 0
                for member in crew:
                    name = member['name']
                    if member['known_for_department'] == 'Directing':
                        print(name + ': ' + member['known_for_department'])
                        if name in director_data:
                            average_director_earnings = average_director_earnings + \
                                int(director_data[name])
                            directors = directors + 1
                        elif (name in producer_data and name not in director_data):
                            average_director_earnings = average_director_earnings + \
                                int(director_data[name])
                            directors = directors + 1
                        else:
                            directors = directors + 1
                    elif member['known_for_department'] == 'Production':
                        print(name + ': ' + member['known_for_department'])
                        if name in producer_data:
                            average_producer_earnings = average_producer_earnings + \
                                int(producer_data[name])
                            producers = producers + 1
                        elif (name in director_data and name not in producer_data):
                            average_producer_earnings = average_producer_earnings + \
                                int(producer_data[name])
                            producers = producers + 1
                        else:
                            producers = producers + 1
                if (producers != 0):
                    average_producer_earnings = average_producer_earnings / producers
                if (directors != 0):
                    average_director_earnings = average_director_earnings / directors

                """
                data = {
                    'Id': movie_id,
                    'Title': movie['title'],
                    'Action': 'Action' in movie_genres,
                    'Adventure': 'Adventure' in movie_genres,
                    'Animation': 'Animation' in movie_genres,
                    'Comedy': 'Comedy' in movie_genres,
                    'Crime': 'Crime' in movie_genres,
                    'Documentary': 'Documentary' in movie_genres,
                    'Drama': 'Drama' in movie_genres,
                    'Family': 'Family' in movie_genres,
                    'Fantasy': 'Fantasy' in movie_genres,
                    'History': 'History' in movie_genres,
                    'Horror': 'Horror' in movie_genres,
                    'Music': 'Music' in movie_genres,
                    'Mystery': 'Mystery' in movie_genres,
                    'Romance': 'Romance' in movie_genres,
                    'Science Fiction': 'Science Fiction' in movie_genres,
                    'TV Movie': 'TV Movie' in movie_genres,
                    'Thriller': 'Thriller' in movie_genres,
                    'War': 'War' in movie_genres,
                    'Western': 'Western' in movie_genres,
                    'Original_Language': movie['original_language'],
                    'Production_company': 1,
                    'Average Director Earnings': average_director_earnings,
                    'Average Producer Earnings': average_producer_earnings,
                    'Average Actor Earnings': average_actor_earnings,
                    'Budget': movie['budget'],
                    'Revenue': movie['revenue'],
                    'Runtime': movie['runtime'],
                    'Adult': movie['adult']
                    }
                """

                csvwriter = csv.writer(csvfile)
                csvwriter.writerow([movie_id, movie['title'], 'Action' in movie_genres, 'Adventure' in movie_genres, 'Animation' in movie_genres,
                                    'Comedy' in movie_genres, 'Crime' in movie_genres, 'Documentary' in movie_genres, 'Drama' in movie_genres,
                                    'Family' in movie_genres, 'Fantasy' in movie_genres, 'History' in movie_genres, 'Horror' in movie_genres,
                                    'Music' in movie_genres, 'Mystery' in movie_genres, 'Romance' in movie_genres, 'Science Fiction' in movie_genres,
                                    'TV Movie' in movie_genres, 'Thriller' in movie_genres, 'War' in movie_genres, 'Western' in movie_genres,
                                    movie['original_language'], 1, average_director_earnings, average_producer_earnings, average_actor_earnings,
                                    movie['budget'], movie['revenue'], movie['runtime'], movie['adult']])
