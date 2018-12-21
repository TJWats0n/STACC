import time, os, math, pickle, schedule
from datetime import datetime, timedelta
from config import Config
from threading import Thread
import pandas as pd
import numpy as np
import analyse_crowded, preprocess_data, detect_crowded, tweet_collection, convertJson


def ceil_dt(dt, delta):
    return datetime.min + math.ceil((dt - datetime.min) / delta) * delta


def get_file(path,file_name):
    # open timeseries file
    try:
        file = open(path + file_name, 'rb')
    except FileNotFoundError("File with path {0} could not be found.".format(path + file_name)):
        quit()
    return pickle.load(file)


def del_raw_data():  # raw_data can be deleted immediately as preprocessing is finished above in converJSON.main()
    for file in os.listdir(Config.data):
        file_path = os.path.join(Config.data, file)
        os.remove(file_path)


def del_prep_data():
    file_pathes = [os.path.join(Config.prep_data, x) for x in os.listdir(Config.prep_data)]
    file_date = sorted(file_pathes, key=os.path.getctime)
    # only keep csf latest files; after running real_time for csf*interval amount of time tweets corpus will be consecutive
    #e.g. csf=4 interval=6, at first static data from 3 months ago, After 24h (4*6) the latest for files will be tweets of last 24h.
    for old_file in file_date[:-Config.corpus_size_factor]:
        os.remove(old_file)


def handler():
    print('Analyse latest data...')
    t = pd.Timestamp(datetime.now())
    latest_bucket = t.floor('{}min'.format(Config.interval))  # Assuming this will be very close to the (but still after) the wished timestamp

    convertJson.main() # transform json format of most recent tweets to csv format

    tweets = preprocess_data.load_data()

    filtered_tweets = preprocess_data.filter_spam(tweets)
    grid_tweets = preprocess_data.calc_grid(filtered_tweets)

    # create_time_series() can be used but here yields only one time slice
    # as the provided data is only the size of one interval
    timeslice, oldest = detect_crowded.create_time_series(grid_tweets)
    timeslice[0][1][1] = 200

    timeseries = get_file(Config.helper_files, 'timeseries.p')

    #uncomment if you want to preserve the timeseries from your static data. timeseries.p will be overwritten for real time mode
    #pickle.dump(timeseries, open(Config.helper_files + 'timeseries_from_static.p', 'wb'))

    sl_window = int((24/(Config.interval/60))*Config.sliding_window) # how many times does interval fit into day * sliding window
    timeseries = np.append(timeseries, timeslice, axis=0)

    pickle.dump(timeseries, open(Config.helper_files + 'timeseries.p', 'wb'))

    if len(timeseries) < Config.sliding_window:
        print('The timeseries is too small to detect crowded places. '
              'Please wait ', Config.sliding_window - len(timeseries), ' intervals more.')
        return

    crowded_places = detect_crowded.determine_crowded_per_cell_timeseries(timeseries, real_time_flag=True)

    if not crowded_places:
        print('No crowded places detected.')
    else:
        first_bucket = latest_bucket - pd.Timedelta(minutes=(len(timeseries) * Config.interval))
        crowded_places = detect_crowded.check_amount_tweets(crowded_places, first_bucket)

        related_events_sample = analyse_crowded.get_details(grid_tweets, crowded_places)
        if not related_events_sample:
            print('No new events detected.')
        else:
            print('HURRAY! New events detected.')
            master_object = get_file(Config.interval, 'master_object.p')
            for key, value in related_events_sample.items():
                master_object[key] = value
            pickle.dump(master_object, open(Config.results+'master_object.p', 'wb'))

    timeseries = timeseries[-sl_window:]  # trim timeseries to sliding window size
    del_raw_data() # some deletion logic for raw data and outdated prep data
    del_prep_data()

    print('Processing for {0} finished. Next analysis is taking place at {1}'.format(latest_bucket, latest_bucket + Config.interval))

def scheduler():
    print('Scheduler started...')
    schedule.every(0.1).minutes.do(handler)

    # schedule.every(Config.interval).minutes.do(handler)

    while 1:
        schedule.run_pending()
        # time.sleep(Config.interval)
        time.sleep(1)

def main():
    scheduler()
    return


    print('Start STACC in real-time mode')

    now = datetime.now()
    start_collect_tweets = ceil_dt(now, timedelta(minutes=Config.interval))
    delay = math.floor((start_collect_tweets - now).total_seconds())

    print('Collection of Tweets will start at {}'.format(start_collect_tweets))

    delay = 10

    thread = Thread(target=tweet_collection.main, args=(delay, ))
    thread.daemon = True # will terminate as well if main is terminated
    thread.start()

    scheduler()


if __name__ == "__main__":
    main()