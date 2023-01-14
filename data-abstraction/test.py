import requests
import datetime
import csv
from bs4 import BeautifulSoup


key = "d1a4982a7803d64c3582894a44ee43e9"

director_names = []
director_average_earnings = []

producer_data = []
producer_average_earnings = []

actor_data = []
actor_average_earnings = []

# URL's for web scraping
director_URL = "https://www.the-numbers.com/box-office-star-records/international/lifetime-specific-technical-role/director"
producer_URL = "https://www.the-numbers.com/box-office-star-records/worldwide/lifetime-specific-technical-role/producer"
actor_URL = "https://www.the-numbers.com/box-office-star-records/worldwide/lifetime-acting/top-grossing-stars"

# Header params
header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
}


def get_director_data():

    # Start director index(Every idx value represents top directors from
    # rank idx - idx + 100. Every 100 directors are on separate pages.)
    idx = 1

    # Loop to all possible director page suffixes.(A suffix in this case is the
    # following '${director_URL}/{suffix}') We stop at 15001 as that is the
    # largest suffix possible for the list of directors
    while idx <= 1:
        # 15001

        # If looking at the first 100 directors, don't append to the URL.
        # index value not required for first 100 directors.
        if idx == 1:
            r = requests.get(director_URL, headers=header)
        # If not looking at the first 100 directors, append to the URL.
        # Index value required for directors not in top 100.
        else:
            r = requests.get(director_URL + '/' + str(idx), headers=header)

        # Parsing data
        soup = BeautifulSoup(r.content, "html.parser")

        # Getting all b tags. All names are nested within <b><b/> tags
        page_data = soup.find_all("b")

        # Getting the name for each director
        for tag in page_data:
            # All name values are contained in <a><a/> tags
            nametags = tag.find_all("a")
            for tag in nametags:
                # If text value is not a name, dont append. Otherwise append.
                if (tag.text != 'Nash Information Services, LLC' and
                        tag.text != 'corrections@the-numbers.com'):
                    director_names.append(tag.text)

        # Getting all td tags. All monetary values are nested within <td><td/> tags
        average_earnings = soup.find_all("td", {"align": "right"})

        # Setting the count value to zero as every third <td></td> tag corresponds
        # to a director's average earnings.
        count = 0
        for tag in average_earnings:
            count = count + 1
            # If every third tag is selected, append.
            if (count % 3 == 0):
                director_average_earnings.append(
                    int(tag.text.replace('$', '').replace(',', '')))

        # Increment to the next page of directors
        idx = idx + 100

    # Save the director name and average earnings to csv file
    with open('director_revenue.csv', 'w', encoding="utf-8", newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['name', 'average_revenue_per_movie'])
        for i in range(len(director_names)):
            csvwriter.writerow(
                [director_names[i], director_average_earnings[i]])


get_director_data()


def get_producer_data():

    # Start producer index(Every idx value represents top producers from
    # rank idx - idx + 100. Every 100 producers are on separate pages.)
    idx = 1

    # Loop to all possible producer page suffixes.(A suffix in this case is the
    # following '${producer_URL}/{suffix}') We stop at 13001 as that is the
    # largest suffix possible for the list of producers.
    while idx <= 13001:

        # If looking at the first 100 producers, don't append to the URL.
        # index value not required for first 100 producers.
        if idx == 1:
            r = requests.get(producer_URL, headers=header)
        # If not looking at the first 100 producers, append to the URL.
        # Index value required for producers not in top 100.
        else:
            r = requests.get(producer_URL + '/' + str(idx), headers=header)

        # Parsing data
        soup = BeautifulSoup(r.content, "html.parser")

        # Getting all b tags. All names are nested within <b><b/> tags
        page_data = soup.find_all("b")

        # Getting the name for each producer
        for tag in page_data:
            # All name values are contained in <a><a/> tags
            nametags = tag.find_all("a")
            for tag in nametags:
                # If text value is not a name, dont append. Otherwise append.
                if (tag.text != 'Nash Information Services, LLC' and
                        tag.text != 'corrections@the-numbers.com'):
                    producer_data.append(tag.text)

        # Getting all td tags. All monetary values are nested within <td><td/> tags
        average_earnings = soup.find_all("td", {"align": "right"})

        # Setting the count value to zero as every third <td></td> tag corresponds
        # to a producer's average earnings.
        count = 0
        for tag in average_earnings:
            count = count + 1
            if (count % 3 == 0):
                producer_average_earnings.append(
                    int(tag.text.replace('$', '').replace(',', '')))

        # Increment to the next page of producers
        idx = idx + 100

    # Save the producer name and average earnings to csv file
    with open('producer_revenue.csv', 'w', encoding="utf-8", newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['name', 'average_revenue_per_movie'])
        for i in range(len(producer_data)):
            csvwriter.writerow(
                [producer_data[i], producer_average_earnings[i]])


def get_actor_data():

    # Start actor index(Every idx value represents top directors from
    # rank idx - idx + 100. Every 100 actors are on separate pages.)
    idx = 1

    # Loop to all possible actor page suffixes.(A suffix in this case is the
    # following '${actor_URL}/{suffix}') We stop at 86401 as that is the
    # largest suffix possible for the list of actors.
    while idx <= 86401:

        # If looking at the first 100 actors, don't append to the URL.
        # index value not required for first 100 actors.
        if idx == 1:
            r = requests.get(actor_URL, headers=header)
        # If not looking at the first 100 actors, append to the URL.
        # Index value required for actors not in top 100.
        else:
            r = requests.get(actor_URL + '/' + str(idx), headers=header)

        # Parsing data
        soup = BeautifulSoup(r.content, "html.parser")

        # Getting all b tags. All names are nested within <b><b/> tags
        data = soup.find_all("b")

        # Getting the name for each actor
        for tag in data:
            # All name values are contained in <a><a/> tags
            nametags = tag.find_all("a")
            for tag in nametags:
                # If text value is not a name, dont append. Otherwise append.
                if (tag.text != 'Nash Information Services, LLC' and
                        tag.text != 'corrections@the-numbers.com'):
                    actor_data.append(tag.text)

        # Getting all td tags. All monetary values are nested within <td><td/> tags
        average_earnings = soup.find_all("td", {"align": "right"})

        # Setting the count value to zero as every third <td></td> tag corresponds
        # to a actor's average earnings.
        count = 0
        for tag in average_earnings:
            count = count + 1
            if (count % 3 == 0):
                actor_average_earnings.append(
                    int(tag.text.replace('$', '').replace(',', '')))

        # Increment to the next page of actors
        idx = idx + 100
        print(str(idx - 1) + " actors completed")

    print(len(actor_data))
    print(len(actor_average_earnings))
    # actor_data = {actor_data[i]: actor_average_earnings[i] for i in range(len(actor_data))}

    # Save the actor name and average earnings to csv file
    with open('actor_revenue.csv', 'w', encoding="utf-8", newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['name', 'average_revenue_per_movie'])
        for i in range(len(actor_data)):
            csvwriter.writerow([actor_data[i], actor_average_earnings[i]])


def movie_ids():
    URL = "https://api.themoviedb.org/3/discover/movie/"

    year = 1940
    month = 1
    day = 1

    movie_ids = []

    while (datetime.date(year, month, day).strftime("%Y/%m/%d") != '2023/02/01'):

        if (datetime.date(year, month, day).strftime("%Y/%m/%d") == '1940/01/01'):
            start_date = datetime.date(year, month, day)
        else:
            start_date = datetime.date(year, month, day+1)

        if month == 12:
            year = year + 1
            month = 1
        else:
            month = month + 1

        end_date = datetime.date(year, month, day)

        print("start date: " + start_date.strftime("%Y/%m/%d"))
        print("end date: " + end_date.strftime("%Y/%m/%d"))
        print("===============================\n===============================")

        PARAMS = {'api_key': key,
                  'primary_release_date.gte': start_date,
                  'primary_release_date.lte': end_date}

        r = requests.get(url=URL, params=PARAMS)
        data = r.json()
        pages = data['total_pages']

        results = len(data['results'])

        for movie in range(results):
            movie_ids.append(data['results'][movie]['id'])

        for x in range(1, pages):
            PARAMS.update({'page': x + 1})
            r = requests.get(url=URL, params=PARAMS)
            data = r.json()
            results = len(data['results'])
            for movie in range(results):
                movie_ids.append(data['results'][movie]['id'])

    with open('test.txt', 'w') as fp:
        for item in movie_ids:
            # write each item on a new line
            fp.write("%s\n" % item)
        print('Done')


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
                                        'Production_company', 'Average Director Earnings',
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
