import pandas as pd
import os
from config import Config
from map_grid import MapGrid
from tqdm import tqdm
import sys


def load_data():
    """
    Loads data from a specified list of paths into dataframe. Lines without lon & lat are omitted.

    :return df: A dataframe of the whole dataset specified with only entries which provide lat & lon.
    """
    if Config.data_type == 'static':
        print('Collecting static data')
        prep_files = [Config.prep_data + document for document in os.listdir(Config.prep_data) if document.find('preprocessed') > 0]
    elif Config.data_type == 'stream':
        print('Collecting stream data')
        files_in_dir = [Config.prep_data + document for document in os.listdir(Config.prep_data)]
        prep_files = max(files_in_dir, key=os.path.getctime()) #in stream scenario only the latest file is needed as others have been processed before
    else:
        sys.exit('Please choose a "data_type" in the config of either "static" or "stream"')


    all_tweets = pd.DataFrame()
    tqdm.write('loading data...')
    for Table in tqdm(prep_files):
        df_tmp = pd.read_table(Table, sep='\t', header=0, parse_dates=["date"], index_col="date")

        # drop all entries which do not have lat & lon
        df_tmp = df_tmp.dropna(subset=["lat", "lon"])

        # filter inconsistencies of specified files
        df_tmp = df_tmp[df_tmp['place_name'].str.contains(Config.city.title(), na=False)]

        # fuse all files into one dataframe
        all_tweets = all_tweets.append(df_tmp)
    return all_tweets


def filter_spam(tweets):

    # apply word from stoplist
    filtered_tweets = tweets[~tweets.text.str.contains("|".join(Config.spam_filter))]

    # filter tweets from 'New York' geo-tag
    filtered_tweets = filtered_tweets.loc[(filtered_tweets['lon'] != 40.714200) & (filtered_tweets['lat'] != -74.006400)]

    # filter bugged tweets
    filtered_tweets = filtered_tweets[~filtered_tweets.text.str.contains("b'\[[0-9][0-9]:[0-9][0-9]:[0-9][0-9]\]")]

    print('Filtering stats - original:', len(tweets), 'filtered:', len(filtered_tweets))
    return filtered_tweets


def calc_grid(tweets, map_size = Config.map_size):

    # MapGrid creates a grid as overlay for a city.
    city_map = MapGrid(Config.city, map_size, map_size)

    # Location of a tweet is translated from latitudes&longitudes to an x,y code which represents one cell in the grid
    tweets["grid"] = tweets.apply(lambda x: city_map.get_grid(x['lat'], x['lon']), axis=1)

    return tweets[tweets['grid'].notnull()]
