import pandas as pd
import numpy as np
from config import Config


# ================================ helper functions ============================================
def get_lengt_of_timeseries(tweets, oldest_tweet, interval=Config.interval):
    time_range = tweets.index.max() - oldest_tweet

    # ceil because the end of data does not fit the intervals seamless but still should be included
    amount_intervalls = int(np.ceil(time_range.total_seconds() / 60 / interval))

    return amount_intervalls

def z_score(mean, std, element):
    return (element-mean)/std

def determine_sliding_window(timeseries):
    sliding_window_size = int((Config.sliding_window * 24 * 60)/Config.interval)

    if sliding_window_size > len(timeseries):
        print('Warning: sliding window is larger as data. Will use all data for sliding window.')
        sliding_window_size = len(timeseries)

    return sliding_window_size

def create_timestamp(timeframe, first_bucket):
    delta = timeframe * Config.interval
    timestamp = first_bucket + pd.Timedelta('{0} min'.format(delta))
    return timestamp

# ================================ main functions ============================================

def create_time_series(tweets, interval=Config.interval, map_size=Config.map_size):
    oldest_tweet = tweets.index.min().floor(freq='1H')
    first_bucket = oldest_tweet + pd.Timedelta('{}m'.format(Config.interval))
    length_timeseries = get_lengt_of_timeseries(tweets, oldest_tweet, interval)

    timeseries = [np.zeros((map_size, map_size), dtype=np.int) for point_of_time in range(int(length_timeseries))]
    timeseries = np.array(timeseries)

    tweets['index'] = tweets.index
    grouped_tweets = tweets.groupby([pd.Grouper(key='index', freq='{0}min'.format(interval), label='right'), 'grid']).count()
    grouped_tweets = grouped_tweets.rename(columns={'text': 'amount_tweets'})

    for index, row in grouped_tweets.iterrows():

        time_difference = index[0] - first_bucket

        # -1 to use it as index, otherwise the last element would be out of bound
        timeframe = int(time_difference.total_seconds() // (60 * interval))

        #fill the timeseries from tweet corpus
        timeseries[timeframe,int(index[1][1]),int(index[1][0])] = row[0]

    return timeseries, first_bucket


def determine_crowded_per_cell_timeseries(timeseries, real_time_flag=False):

    crowded_cells = {}
    window_size = determine_sliding_window(timeseries)

    for y in range(Config.map_size):
        for x in range(Config.map_size):
            cell_timeseries = []

            if real_time_flag == False:
                for timeframe in range(len(timeseries)):
                    cell_timeseries.append(timeseries[timeframe][y][x])
            else:#check only the last frame
                for timeframe in range(len(timeseries)-window_size,len(timeseries),1):
                    cell_timeseries.append(timeseries[timeframe][y][x])

            #use only practical distributions
            if len(cell_timeseries)/2 < cell_timeseries.count(0):
                continue

            for index, amount_tweets in enumerate(cell_timeseries):
                if index < window_size:
                    mean = np.mean(cell_timeseries[:window_size])
                    std = np.std(cell_timeseries[:window_size])
                else:
                    mean = np.mean(cell_timeseries[(index - window_size):index])
                    std = np.std(cell_timeseries[(index - window_size):index])

                if amount_tweets < mean:
                    continue
                if 3 < z_score(mean, std, amount_tweets):
                    crowded_cells[(index, x, y)] = amount_tweets

    return crowded_cells


def check_amount_tweets(crowded_cells, first_bucket):
    crowded_places = []

    for index_grid, amount_tweets in crowded_cells.items():
        timeframe = int(index_grid[0])

        if amount_tweets > 50:
            timestamp = create_timestamp(timeframe, first_bucket)
            crowded_places.append((timestamp, (float(index_grid[1]), float(index_grid[2])), amount_tweets))

    return crowded_places




