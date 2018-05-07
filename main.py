import preprocess_data
import config
import analyse_crowded
import detect_crowded
import convertJson







# ================================== Phase 1 - Load data ==========================================================


if config.Config.data_type == 'static':

    #transform tweets from JSON to csv format
    convertJson.main()

    tweets = preprocess_data.load_data()

    tweets = preprocess_data.filter_spam(tweets)

    tweets = preprocess_data.calc_grid(tweets)

if config.Config.data_type == 'stream':
    # implement stream here



# ================================== Phase 2 - Detect Crowded =====================================================




#================================== Phase 3 - Analyse Crowded =====================================================