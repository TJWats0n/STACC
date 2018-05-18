import preprocess_data
import config
import detect_crowded
import convertJson
import analyse_crowded
import pandas as pd
import ast
import pickle

temp_files = 'other_files/'

# ================================== Phase 1 - Load data ==========================================================

# #transform tweets from JSON to csv format
# #convertJson.main()

previous_map_size = pickle.load(open('other_files/previous_map_size.p', 'rb'))

if previous_map_size != config.Config.map_size:
    print('Mapsize was changed, therefore data must be preprocessed again. This can take a minute or two.')

    tweets = preprocess_data.load_data()

    tweets = preprocess_data.filter_spam(tweets)

    tweets = preprocess_data.calc_grid(tweets)

    tweets.to_csv(temp_files+'tweets.csv', sep='\t', encoding='utf-8')

    pickle.dump(config.Config.map_size, open(temp_files+'previous_map_size.p', 'wb'))

# ================================== Phase 2 - Detect Crowded =====================================================
print('Detecting crowd...')

tweets = pd.read_csv(temp_files+'tweets.csv',
                         parse_dates={'datetime': ['date']},
                         converters={'grid': ast.literal_eval},  # without pandas would load tuple as type string
                         index_col='datetime',
                         sep='\t')

timeseries, first_bucket = detect_crowded.create_time_series(tweets)

crowded_places = detect_crowded.determine_crowded_per_cell_timeseries(timeseries)

crowded_places = detect_crowded.check_amount_tweets(crowded_places, first_bucket)

pickle.dump(crowded_places, open(temp_files+'cp.p','wb'))


#================================== Phase 3 - Analyse Crowded =====================================================
print('Analyse crowd...')

crowded_places = pickle.load(open(temp_files+'cp.p', 'rb'))

tweets = pd.read_csv(temp_files+'tweets.csv',
                         parse_dates={'datetime': ['date']},
                         converters={'grid': ast.literal_eval},  # without pandas would load tuple as type string
                         index_col='datetime',
                         sep='\t')

related_events_sample = analyse_crowded.get_details(tweets, crowded_places)
print('end')