import schedule
import time
from datetime import datetime, timedelta
from config import Config
from cloudant.client import Cloudant
from requests.adapters import HTTPAdapter
from cloudant.query import Query
from real_time_config import RTConfig
import pandas as pd
import numpy as np
import math
import analyse_crowded, preprocess_data, detect_crowded, tweet_collection
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

def get_tweets_with_geo(database, until_then):
    df = pd.DataFrame()
    from_then = until_then - pd.Timedelta(minutes=Config.interval)
    RTConfig.selector['created_at']['$gte'] = from_then.strftime('%a %b %d %H:%M:%S +0000 %Y')
    RTConfig.selector['created_at']['$lte'] = until_then.strftime('%a %b %d %H:%M:%S +0000 %Y')
    query = Query(database, selector=RTConfig.selector, fields=RTConfig.fields)

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

def get_file(path,file_name):
    # open timeseries file
    try:
        file = open(path + file_name, 'rb')
    except FileNotFoundError:
        file = open(path + file_name, 'rb')

    return pickle.load(file)

def handler():
    t = pd.Timestamp(datetime.now())
    latest_bucket = t.floor('{}min'.format(Config.interval)) #Assuming this will be very close to the (but still after) the wished timestamp
    print('Analyse latest data.')
    database = connect_to_db()
    tweets = get_tweets_with_geo(database,latest_bucket)
    filtered_tweets = preprocess_data.filter_spam(tweets)
    grid_tweets = preprocess_data.calc_grid(filtered_tweets)

    #create_time_series() can be used but here yields only one time slice
    # as the provided data is only the size of one interval
    timeslice, oldest = detect_crowded.create_time_series(grid_tweets)

    timeseries = get_file('other_files/', 'timeseries.p')

    np.append(timeseries, timeslice, axis=0)

    if len(timeseries) < Config.sliding_window:
        print('The timeseries is to small to detect crowded places. '
              'Please wait ', Config.sliding_window - len(timeseries), ' intervals more.')
        return

    crowded_places = detect_crowded.determine_crowded_per_cell_timeseries(timeseries, real_time_flag=True)

    first_bucket = latest_bucket - pd.Timedelta(minutes=(len(timeseries) * Config.interval))
    crowded_places = detect_crowded.check_amount_tweets(crowded_places, first_bucket)
    related_events_sample = analyse_crowded.get_details(grid_tweets, crowded_places)

    if related_events_sample is None:
        print('No new crowded places detected.')
        return

    print('sth')
    master_object = get_file(Config.interval, 'master_object.p')

    for key, value in related_events_sample.items():
        master_object[key]=value

    pickle.dump(master_object, open(Config.results+'master_object.p', 'wb'))

    print('Processing for {0} finished. Next analysis is taking place at {1}'.format(latest_bucket, latest_bucket+Config.interval))

def scheduler():
    print('Scheduler started...')
    # schedule.every(1).minutes.do(handler)

    schedule.every(Config.interval).minutes.do(handler)

    while 1:
        schedule.run_pending()
        time.sleep(Config.interval)
        # time.sleep(1)

def main():
    print('start')

    now = datetime.now()
    start_collect_tweets = ceil_dt(now, timedelta(minutes=Config.interval))
    delay = (start_collect_tweets - now).total_seconds()

    print('Collection of tweets will start at {}'.format(start_collect_tweets))

    # delay = 0

    t = threading.Timer(delay, tweet_collection.main())
    t.daemon=True
    t.start()

    # delay + Config.interval

    threading.Timer(0, scheduler).start()

if __name__ == "__main__":
    main()