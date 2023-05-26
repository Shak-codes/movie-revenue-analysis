from scrape import scrape_movie

# URL's for web scraping
director_URL = "https://www.the-numbers.com/box-office-star-records/international/lifetime-specific-technical-role/director"
producer_URL = "https://www.the-numbers.com/box-office-star-records/worldwide/lifetime-specific-technical-role/producer"
actor_URL = "https://www.the-numbers.com/box-office-star-records/worldwide/lifetime-acting/top-grossing-stars"
production_company_URL = "https://www.the-numbers.com/movies/production-companies#production_companies_overview=od1"

director_largest_idx = 15001
producer_largest_idx = 13001
actor_largest_idx = 86501

scrape_movie(director_URL, director_largest_idx,
             'C:\\Users\\shaki\\Documents\\GitHub\\movie-revenue-analysis\\data\\director_data.csv')
print("Directors done!")
scrape_movie(producer_URL, producer_largest_idx,
             'C:\\Users\\shaki\\Documents\\GitHub\\movie-revenue-analysis\\data\\producer_data.csv')
print("Producers done!")
scrape_movie(actor_URL, actor_largest_idx,
             'C:\\Users\\shaki\\Documents\\GitHub\\movie-revenue-analysis\\data\\actor_data.csv')
print("Actors done!")
