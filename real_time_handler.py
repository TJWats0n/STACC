import schedule
import time
from datetime import datetime, timedelta
from config import Config
import pandas as pd
import numpy as np
import math
import analyse_crowded, preprocess_data, detect_crowded, tweet_collection, convertJson
import threading
import pickle

def ceil_dt(dt, delta):
    return datetime.min + math.ceil((dt - datetime.min) / delta) * delta

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

    convertJson.main() #transform json format of most recent tweets to csv format

    tweets = preprocess_data.load_data()

    filtered_tweets = preprocess_data.filter_spam(tweets)
    grid_tweets = preprocess_data.calc_grid(filtered_tweets)

    #create_time_series() can be used but here yields only one time slice
    # as the provided data is only the size of one interval
    timeslice, oldest = detect_crowded.create_time_series(grid_tweets)

    timeseries = get_file(Config.helper_files, 'timeseries.p')

    np.append(timeseries, timeslice, axis=0)

    #remove first timeframe of timeseries to keep consistent length

    if len(timeseries) < Config.sliding_window:
        print('The timeseries is too small to detect crowded places. '
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
        master_object[key] = value

    pickle.dump(master_object, open(Config.results+'master_object.p', 'wb'))

    #some deletion logic for raw data and outdated prep data

    print('Processing for {0} finished. Next analysis is taking place at {1}'.format(latest_bucket, latest_bucket + Config.interval))

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