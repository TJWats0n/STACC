import pandas as pd
import numpy as np
from config import Config


# ================================ helper functions ============================================
def get_lengt_of_timeseries(tweets, oldest_tweet, interval=Config.interval):
    time_range = tweets.index.max() - oldest_tweet

    # +1 because the end of data does not fit the intervals seamless but still should be included
    amount_intervalls = int(time_range.total_seconds() / 60 / interval) + 1

    return amount_intervalls

def z_score(mean, std, element):
    return (element-mean)/std

def determine_sliding_window(timeseries):
    sliding_window_size = (Config.sliding_window * 24 * 60)/Config.interval

    if sliding_window_size > len(timeseries):
        print('Warning: sliding window is larger as data. Will use all data for sliding window.')
        sliding_window_size = len(timeseries)

    return sliding_window_size

def create_timestamp(timeframe, oldest):
    delta = timeframe * Config.interval
    timestamp = oldest + pd.Timedelta('{0} min'.format(delta))
    return timestamp

# ================================ main functions ============================================

def create_time_series(tweets, interval=Config.interval, map_size=Config.map_size):
    oldest_tweet = tweets.index.min().floor(freq='1H')
    length_timeseries = get_lengt_of_timeseries(tweets, oldest_tweet, interval)

    timeseries = [np.zeros((map_size, map_size), dtype=np.int) for point_of_time in range(int(length_timeseries))]
    timeseries = np.array(timeseries)

    tweets['index'] = tweets.index
    grouped_tweets = tweets.groupby([pd.Grouper(key='index', freq='{0}min'.format(interval), label='right'), 'grid']).count()
    grouped_tweets = grouped_tweets.rename(columns={'text': 'amount_tweets'})

    for index, row in grouped_tweets.iterrows():

        time_difference = index[0] - oldest_tweet

        # -1 to use it as index, otherwise the last element would be out of bound
        timeframe = int(time_difference.total_seconds() // (60 * interval)) -1

        #fill the timeseries from tweet corpus
        timeseries[timeframe,int(index[1][1]),int(index[1][0])] = row[0]

    #timeseries = timeseries[1:,:,:]

    return timeseries, oldest_tweet


def determine_crowded_per_cell_timeseries(timeseries):

    crowded_cells = {}
    historic_window_size = determine_sliding_window(timeseries)

    for y in range(Config.map_size):
        for x in range(Config.map_size):
            cell_timeseries = []

            for timeframe in range(len(timeseries) - historic_window_size,len(timeseries), 1):
                cell_timeseries.append(timeseries[timeframe][y][x])

            #use only practical distributions
            if len(cell_timeseries)/2 < cell_timeseries.count(0):
                continue

            mean = np.mean(cell_timeseries)
            std = np.std(cell_timeseries)

            for index, amount_tweets in enumerate(cell_timeseries):
                if amount_tweets < mean:
                    continue
                if 3 < z_score(mean, std, amount_tweets):
                    crowded_cells[(index, x, y)] = amount_tweets

    return crowded_cells


def determine_crowded_per_timeframe(crowded_cells, timeseries, oldest_tweets):
    crowded_places = []

    #create distribution of timeframe a crowded cell appears in, calculate std and compare std to crowded cell value
    for index_grid, amount_tweets in crowded_cells.items():
        timeframe = int(index_grid[0])
        timeframe_distribution = []

        for y in range(Config.map_size):
            for x in range(Config.map_size):
                timeframe_distribution.append(timeseries[timeframe][y][x])

        std = np.std(timeframe_distribution)

        if amount_tweets > (3 * std):
            timestamp = create_timestamp(timeframe, oldest_tweets)
            crowded_places.append((timestamp, (float(index_grid[1]), float(index_grid[2])), amount_tweets))

    return crowded_places
