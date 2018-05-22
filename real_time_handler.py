import schedule
import time
from datetime import datetime
from datetime import timedelta
from config import Config
from cloudant.client import Cloudant
from requests.adapters import HTTPAdapter
from cloudant.query import Query
from real_time_config import RTConfig
import pandas as pd
import math
import preprocess_data
import detect_crowded
import threading
import pickle

def ceil_dt(dt, delta):
    return datetime.min + math.ceil((dt - datetime.min) / delta) * delta

def connect_to_db():
    cloudant_cred = RTConfig.cloudant_cred
    httpAdapter = HTTPAdapter(pool_connections=15, pool_maxsize=100)
    client = Cloudant(cloudant_cred['username'], cloudant_cred['password'], url=cloudant_cred['url'],
                      connect=True,
                      adapter=httpAdapter)

    database = client['streamed_tweets']
    return database

def get_tweets_with_geo(database):
    df = pd.DataFrame()
    query = Query(database, selector=RTConfig.selector, fields=RTConfig.fields)

    #the time selection must be still integrated in the selector

    with query.custom_result() as rslt:
        for entry in rslt:
            df = df.append({'screen_name': entry["user"]["screen_name"],
                            "text": entry["text"],
                            "timestamp": entry["created_at"],
                            "lon": entry["geo"]["coordinates"][0],
                            "lat": entry["geo"]["coordinates"][1]},
                           ignore_index=True
                           )

    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%a %b %d %H:%M:%S +%f %Y')
    df.set_index('timestamp', inplace=True)
    return df

def handler():
    print('Analyse latest data.')
    database = connect_to_db()
    tweets = get_tweets_with_geo(database)
    filtered_tweets = preprocess_data.filter_spam(tweets)
    grid_tweets = preprocess_data.calc_grid(filtered_tweets)

    #create_time_series() can be used but here yields only one time slice
    # as the provided data is only the size of one interval
    timeslice, oldest = detect_crowded.create_time_series(grid_tweets)
    timeslice = timeslice[1]

    #open timeseries file
    try:
        file = open('other_files/timeseries.p', 'rb')
    except FileNotFoundError:
        file = open('other_files/timeseries.p', 'wb')

    timeseries = pickle.load(file)

    if len(timeseries) < Config.sliding_window:

        #try to construct from files
        #saving tweets to files ensures to rerun the real_time set up with different interval without waiting for 30 days again

        print('The timeseries is to small to detect crowded places. '
              'Please wait ', Config.sliding_window - len(timeseries), ' intervals more.')
        return

    crowded_places = detect_crowded.determine_crowded_per_cell_timeseries(timeseries,
                                                                          real_time_flag=True,
                                                                          timeslice=timeslice)
    # crowded_places = detect_crowded...
    print('sth')


def scheduler():
    print('Scheduler started...')
    schedule.every(1).minutes.do(handler)

    while 1:
        schedule.run_pending()
        time.sleep(1)

def start_tweet_collection():
    print('sth')


def main():
    print('start')

    now = datetime.now()
    start_collect_tweets = ceil_dt(now, timedelta(minutes=Config.interval))
    delay = (start_collect_tweets - now).total_seconds()

    print('Collection of tweets will start at {}'.format(start_collect_tweets))

    delay = 0

    t = threading.Timer(delay, start_tweet_collection)
    t.daemon=True
    t.start()

    threading.Timer(delay + Config.interval, scheduler).start()

if __name__ == "__main__":
    main()