import requests
from datetime import datetime
import csv
import time

key = "d1a4982a7803d64c3582894a44ee43e9"
PATH = 'C:\\Users\\shaki\\Documents\\GitHub\\movie-revenue-analysis\\data\\'
date_format = "%Y-%m-%d"
today = datetime.strptime("2023-01-24", date_format)

# Get data for all movies from start_idx to stop_idx(non-inclusive)


def get_movie_data(start_idx, stop_idx, file_name):

    # Define params
    PARAMS = {'api_key': key}

    # Open actor data and save into dictionary
    with open(PATH + 'actor_data.csv', mode='r', encoding="utf-8") as infile:
        reader = csv.reader(infile)
        actor_data = {rows[0]: rows[1] for rows in reader}
    # Open producer data and save into dictionary
    with open(PATH + 'producer_data.csv', mode='r', encoding="utf-8") as infile:
        reader = csv.reader(infile)
        producer_data = {rows[0]: rows[1] for rows in reader}
    # Open director data and save into dictionary
    with open(PATH + 'director_data.csv', mode='r', encoding="utf-8") as infile:
        reader = csv.reader(infile)
        director_data = {rows[0]: rows[1] for rows in reader}
    # Open production company data and save into dictionary
    with open(PATH + 'production_company_data.csv', mode='r', encoding="utf-8") as infile:
        reader = csv.reader(infile)
        production_company_data = {rows[0]: rows[1] for rows in reader}

    # Open data file to store movie data
    with open(PATH + file_name, 'w', encoding="utf-8", newline='') as csvfile:
        csvwriter = csv.writer(csvfile)

        # Only write column names if the first file
        if start_idx == 0:
            csvwriter.writerow(['Id', 'Title', 'Action', 'Adventure', 'Animation',
                                'Comedy', 'Crime', 'Documentary', 'Drama', 'Family',
                                'Fantasy', 'History', 'Horror', 'Music',
                                'Mystery', 'Romance', 'Science Fiction', 'TV Movie',
                                'Thriller', 'War', 'Western', 'Average Production Company Earnings',
                                'Average Director Earnings', 'Average Producer Earnings',
                                'Average Actor Earnings', 'Budget', 'Revenue', 'Runtime', 'Days Since Release'])

        file = open(PATH + 'movie_ids.csv', 'r')
        movie_ids = file.readlines()

        for idx in range(start_idx, stop_idx):

            # Get movie id
            movie_id = movie_ids[idx].strip()

            # Define base movie URL for every movie_id
            URL = "https://api.themoviedb.org/3/movie/" + movie_id

            # Attempt API call
            try:
                r = requests.get(url=URL, params=PARAMS)
            # Call may fail if too many requests are made too quickly
            # Wait one minute and try again
            except:
                print('Base URL error for id: ' +
                      movie_id + '... Waiting one minute\n')
                time.sleep(60)
                r = requests.get(url=URL, params=PARAMS)

            # Get movie_data
            movie_data = r.json()

            if 'success' not in movie_data:

                # Get days since release
                if movie_data['release_date'] != '':
                    release_date = datetime.strptime(
                        movie_data['release_date'], date_format)
                    days_since_release = today - release_date
                    days_since_release = int(days_since_release.days)
                else:
                    days_since_release = 0

                # Get production companies
                production_companies = []
                for company in movie_data['production_companies']:
                    production_companies.append(company['name'])

                # Get the combined average earnings of the production companies
                average_production_company_earnings = 0
                for company in production_companies:
                    if company in production_company_data:
                        average_production_company_earnings = average_production_company_earnings + \
                            float(production_company_data[company])
                if len(production_companies) != 0:
                    average_production_company_earnings = average_production_company_earnings / \
                        len(production_companies)

                # Get all movie genres
                movie_genres = []
                for genre in range(len(movie_data['genres'])):
                    movie_genres.append(movie_data['genres'][genre]['name'])

                # Update URL
                URL = URL + '/credits'

                # Attempt API call
                try:
                    r = requests.get(url=URL, params=PARAMS)
                # Call may fail if too many requests are made too quickly
                # Wait one minute and try again
                except:
                    print('Credits URL error for ' +
                          str(movie_id) + '(' + movie_data['title'] + ')... Waiting one minute\n')
                    time.sleep(60)
                    r = requests.get(url=URL, params=PARAMS)

                # Get cast and crew data
                credits = r.json()
                if 'cast' in credits and 'crew' in credits:
                    cast = credits['cast']
                    crew = credits['crew']

                    # Get combined average earnings for all actors
                    average_actor_earnings = 0
                    actors = 0
                    for member in cast:
                        name = member['name']
                        if member['character'] != None and member['character'] != "" and '(uncredited)' not in member['character']:
                            if name in actor_data:
                                average_actor_earnings = average_actor_earnings + \
                                    float(actor_data[name])
                            elif name in director_data:
                                average_actor_earnings = average_actor_earnings + \
                                    float(director_data[name])
                            elif name in producer_data:
                                average_actor_earnings = average_actor_earnings + \
                                    float(producer_data[name])
                            actors = actors + 1
                    if (actors != 0):
                        average_actor_earnings = average_actor_earnings / actors

                    # Get combined average earnings for all directors and producers
                    average_director_earnings = 0
                    directors = 0
                    average_producer_earnings = 0
                    producers = 0

                    for member in crew:
                        name = member["name"]
                        department = member["department"]
                        if department == "Directing":
                            if name in director_data:
                                # print('director: ' + str(director_data[name]))
                                average_director_earnings = average_director_earnings + \
                                    float(director_data[name])
                            elif name in producer_data:
                                # print('producer: ' + str(producer_data[name]))
                                average_director_earnings = average_director_earnings + \
                                    float(producer_data[name])
                            directors = directors + 1
                        elif department == "Production":
                            if name in producer_data:
                                average_producer_earnings = average_producer_earnings + \
                                    float(producer_data[name])
                            elif name in director_data:
                                average_producer_earnings = average_producer_earnings + \
                                    float(director_data[name])
                            producers = producers + 1

                    if (directors != 0):
                        average_director_earnings = average_director_earnings / directors
                    if (producers != 0):
                        average_producer_earnings = average_producer_earnings / producers

                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow([movie_id, movie_data['title'], 'Action' in movie_genres, 'Adventure' in movie_genres, 'Animation' in movie_genres,
                                        'Comedy' in movie_genres, 'Crime' in movie_genres, 'Documentary' in movie_genres, 'Drama' in movie_genres,
                                        'Family' in movie_genres, 'Fantasy' in movie_genres, 'History' in movie_genres, 'Horror' in movie_genres,
                                        'Music' in movie_genres, 'Mystery' in movie_genres, 'Romance' in movie_genres, 'Science Fiction' in movie_genres,
                                        'TV Movie' in movie_genres, 'Thriller' in movie_genres, 'War' in movie_genres, 'Western' in movie_genres,
                                        average_production_company_earnings, average_director_earnings, average_producer_earnings,
                                        average_actor_earnings, movie_data['budget'], movie_data['revenue'], movie_data['runtime'], days_since_release])
                else:
                    print(movie_id + ' not written!')
            else:
                print(movie_id + ' not written!')

    print('Completed!')
