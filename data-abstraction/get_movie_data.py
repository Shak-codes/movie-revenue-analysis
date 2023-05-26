import shutil
import threading
from movie_data import get_movie_data

PATH = 'C:\\Users\\shaki\\Documents\\GitHub\\movie-revenue-analysis\\data\\'

# thread1 = threading.Thread(target=get_movie_data,
#                            args=(0, 25000, 'movie_data_1.csv'))
# thread2 = threading.Thread(target=get_movie_data,
#                            args=(25000, 50000, 'movie_data_2.csv'))
# thread3 = threading.Thread(target=get_movie_data,
#                            args=(50000, 75000, 'movie_data_3.csv'))
# thread4 = threading.Thread(target=get_movie_data,
#                            args=(75000, 100000, 'movie_data_4.csv'))
# thread5 = threading.Thread(target=get_movie_data,
#                            args=(100000, 125000, 'movie_data_5.csv'))
# thread6 = threading.Thread(target=get_movie_data,
#                            args=(125000, 150000, 'movie_data_6.csv'))
# thread7 = threading.Thread(target=get_movie_data,
#                            args=(150000, 175000, 'movie_data_7.csv'))
# thread8 = threading.Thread(target=get_movie_data,
#                            args=(175000, 200000, 'movie_data_8.csv'))
# thread9 = threading.Thread(target=get_movie_data,
#                            args=(200000, 225000, 'movie_data_9.csv'))
# thread10 = threading.Thread(target=get_movie_data,
#                             args=(225000, 250000, 'movie_data_10.csv'))
# thread11 = threading.Thread(target=get_movie_data,
#                             args=(250000, 275000, 'movie_data_11.csv'))
# thread12 = threading.Thread(target=get_movie_data,
#                             args=(275000, 300000, 'movie_data_12.csv'))
# thread13 = threading.Thread(target=get_movie_data,
#                             args=(300000, 325000, 'movie_data_13.csv'))
# thread14 = threading.Thread(target=get_movie_data,
#                             args=(325000, 350000, 'movie_data_14.csv'))
# thread15 = threading.Thread(target=get_movie_data,
#                             args=(350000, 375000, 'movie_data_15.csv'))
# thread16 = threading.Thread(target=get_movie_data,
#                             args=(375000, 409740, 'movie_data_16.csv'))

# thread1.start()
# thread2.start()
# thread3.start()
# thread4.start()
# thread5.start()
# thread6.start()
# thread7.start()
# thread8.start()
# thread9.start()
# thread10.start()
# thread11.start()
# thread12.start()
# thread13.start()
# thread14.start()
# thread15.start()
# thread16.start()

# thread1.join()
# thread2.join()
# thread3.join()
# thread4.join()
# thread5.join()
# thread6.join()
# thread7.join()
# thread8.join()
# thread9.join()
# thread10.join()
# thread11.join()
# thread12.join()
# thread13.join()
# thread14.join()
# thread15.join()
# thread16.join()

with open(PATH + 'movie_data.csv', 'wb') as wfd:
    for f in [
            PATH + 'movie_data_1.csv', PATH + 'movie_data_2.csv', PATH +
        'movie_data_3.csv', PATH + 'movie_data_4.csv',
            PATH + 'movie_data_5.csv',  PATH + 'movie_data_6.csv', PATH +
        'movie_data_7.csv', PATH + 'movie_data_8.csv',
            PATH + 'movie_data_10.csv', PATH + 'movie_data_11.csv', PATH +
        'movie_data_12.csv', PATH + 'movie_data_9.csv',
            PATH + 'movie_data_13.csv', PATH + 'movie_data_14.csv', PATH +
        'movie_data_15.csv', PATH + 'movie_data_16.csv',
            PATH + 'movie_data_17.csv']:
        with open(f, 'rb') as fd:
            shutil.copyfileobj(fd, wfd)

# get_movie_data(400086, 409740, 'movie_data_17.csv')
