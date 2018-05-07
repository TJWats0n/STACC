from config import Config
import pandas as pd
import os

def spatial_selection(place, tweets):
    xmax, xmin, ymax, ymin = get_boundaries(place[1], Config.radius)

    spatial_rel_tweets = tweets[tweets['gridx'].between(xmin, xmax, inclusive=True)]
    return spatial_rel_tweets[spatial_rel_tweets['gridy'].between(ymin, ymax, inclusive=True)]

def get_boundaries(position, radius):

    if position[0] + radius > Config.map_size:
        xmax = Config.map_size
    else:
        xmax = position[0] + radius

    if position[0] - radius < 0:
        xmin = 0
    else:
        xmin = position[0] - radius


    if position[1] + radius > Config.map_size:
        ymax = Config.map_size
    else:
        ymax = position[1] + radius

    if position[1] - radius < 0:
        ymin = 0
    else:
        ymin = position[1] - radius

    return xmax, xmin, ymax, ymin

def temporal_selection(place, tweets):
    end_time = place[0]
    start_time = end_time - pd.Timedelta('{0}Min'.format(Config.interval * Config.corpus_size_factor))

    temporal_spatial_rel_tweets = tweets[str(start_time):str(end_time)]
    temporal_spatial_rel_tweets.index.names = ['date']
    return temporal_spatial_rel_tweets

def data_prep(tweets):
    tweets[['gridx', 'gridy']] = pd.DataFrame(tweets['grid'].tolist(), index=tweets.index)
    tweets.drop('grid', axis=1, inplace=True)
    tweets[['gridx', 'gridy']] = tweets[['gridx', 'gridy']].astype(int)
    return tweets

def run_pyMABED(file_name):

    cmd_detect_events = 'python detect_events.py --o pyMABED_visu.p ' +\
                   '../' + Config.results + file_name + ' ' + str(Config.num_topics)

    cmd_built_ui = 'python build_event_browser.py --o ../' + Config.results+ '/visu pyMABED_visu.p'

    os.system(cmd_detect_events)
    os.system(cmd_built_ui)
    print('pyMABED is done.')

def main(tweets, crowded_places):
    tweets = data_prep(tweets)
    file_name = 'related_tweets.csv'
    os.chdir("pyMABED/")

    for entry in crowded_places:
        related_tweets = spatial_selection(entry, tweets)
        related_tweets = temporal_selection(entry, related_tweets)

        related_tweets.to_csv('../'+Config.results + file_name, sep='\t', encoding='utf-8')

        run_pyMABED(file_name)






