import preprocess_data
import config
import detect_crowded
import convertJson
import analyse_crowded
import pandas as pd
import ast
from tqdm import tqdm
import pickle


# ================================== Phase 1 - Load data ==========================================================


if config.Config.data_type == 'static':
    tqdm.write('Phase 1')
    with tqdm(total=4) as pbar:

        #transform tweets from JSON to csv format
        #convertJson.main()

        tweets = preprocess_data.load_data()
        tqdm.write('Phase 1')
        pbar.update(1)

        tweets = preprocess_data.filter_spam(tweets)
        tqdm.write('Phase 1')
        pbar.update(1)

        tweets = preprocess_data.calc_grid(tweets)
        tqdm.write('Phase 1')
        pbar.update(1)

        tweets.to_csv('tweets.csv', sep='\t', encoding='utf-8')
        tqdm.write('Phase 1')
        pbar.update(1)

# if config.Config.data_type == 'stream':
    # implement stream here

# ================================== Phase 2 - Detect Crowded =====================================================
    print('Detecting crowd...')

    timeseries, oldest_tweet = detect_crowded.create_time_series(tweets)

    crowded_places = detect_crowded.determine_crowded_per_cell_timeseries(timeseries)

    crowded_places = detect_crowded.determine_crowded_per_timeframe(crowded_places,timeseries, oldest_tweet)

    pickle.dump(crowded_places, open('cp.p','wb'))


#================================== Phase 3 - Analyse Crowded =====================================================
    print('Analyse crowd...')
    crowded_places = pickle.load(open('cp.p', 'rb'))

    tweets = pd.read_csv('tweets.csv',
                             parse_dates={'datetime': ['date']},
                             converters={'grid': ast.literal_eval},  # without pandas would load tuple as type string
                             index_col='datetime',
                             sep='\t')

    related_events_sample = analyse_crowded.get_details(tweets, crowded_places)
print('end')