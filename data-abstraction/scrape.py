import requests
import csv
from bs4 import BeautifulSoup


def scrape_movie(URL, largest_idx, csv_file):

    names = []
    average_earnings = []

    # Header params
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    }

    # Loop to all possible page suffixes.(A suffix in this case is the
    # following '${URL}/{suffix}') We stop at largest_idx + 1 as that
    # is the largest suffix possible for the list of individuals, and
    # the +1 is because the for loop is not inclusive.
    for idx in range(1, largest_idx + 1, 100):

        # If looking at the first 100 individuals, don't append to the URL.
        # index value not required for first 100 individuals.
        if idx == 1:
            r = requests.get(URL, headers=header)
        # If not looking at the first 100 individuals, append to the URL.
        # Index value required for individuals not in top 100.
        else:
            r = requests.get(URL + '/' + str(idx), headers=header)

        # Parsing data
        soup = BeautifulSoup(r.content, "html.parser")

        # Getting all b tags. All names are nested within <b><b/> tags
        page_data = soup.find_all("b")

        # Getting the name for each individual
        for tag in page_data:
            # All name values are contained in <a><a/> tags
            nametags = tag.find_all("a")
            for tag in nametags:
                # If text value is not a name, dont append. Otherwise append.
                if (tag.text != 'Nash Information Services, LLC' and
                        tag.text != 'corrections@the-numbers.com'):
                    names.append(tag.text)

        # Getting all td tags. All monetary values are nested within <td><td/> tags
        earnings = soup.find_all("td", {"align": "right"})

        # Setting the count value to zero as every third <td></td> tag corresponds
        # to a individual's average earnings.
        count = 1
        for tag in earnings:
            # If every third tag is selected, append.
            if (count % 3 == 0 and type(tag) != int):
                average_earnings.append(
                    int(tag.text.replace('$', '').replace(',', '')))
            count = count + 1

    print(len(names))
    print(len(average_earnings))

    # Save the individual's name and average earnings to csv file
    with open(csv_file, 'w', encoding="utf-8", newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['name', 'average_revenue_per_movie'])
        for i in range(len(names)):
            csvwriter.writerow(
                [names[i], average_earnings[i]])


def scrape_production_companies():
    names = []
    total_earnings = []
    total_movies = []
    average_earnings = []

    URL = "https://www.the-numbers.com/movies/production-companies#production_companies_overview=od1"

    # Header params
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    }

    # Make request
    r = requests.get(URL, headers=header)

    # Parsing data
    soup = BeautifulSoup(r.content, "html.parser")

    # Getting all b tags. All names are nested within <b><b/> tags
    page_data = soup.find_all("b")

    # Getting the name for each individual
    for tag in page_data:
        # All name values are contained in <a><a/> tags
        nametags = tag.find_all("a")
        for tag in nametags:
            # If text value is not a name, dont append. Otherwise append.
            if (tag.text != 'Nash Information Services, LLC' and
                    tag.text != 'corrections@the-numbers.com'):
                names.append(tag.text)

    # Getting all td tags. All monetary values are nested within <td><td/> tags
    production_company_data = soup.find_all("td", {"align": "right"})

    # Setting the count value to zero as every third <td></td> tag corresponds
    # to a individual's average earnings.
    count = 1
    for tag in production_company_data:
        # If every third tag is selected, append.
        if (count % 3 == 0 and type(tag) != int):
            total_earnings.append(
                int(tag.text.replace('$', '').replace(',', '')))
        elif (count % 3 == 1 and type(tag) != int):
            total_movies.append(
                int(tag.text.replace('$', '').replace(',', '')))
        count = count + 1

    for idx in range(len(total_earnings)):
        average_earnings.append(total_earnings[idx]/total_movies[idx])

    # Save the individual's name and average earnings to csv file
    with open('C:\\Users\\shaki\\Documents\\GitHub\\movie-revenue-analysis\\data\\production_company_data.csv', 'w', encoding="utf-8", newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['name', 'average_revenue_per_movie'])
        for i in range(len(names)):
            csvwriter.writerow(
                [names[i], average_earnings[i]])


scrape_production_companies()
