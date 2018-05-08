from config import Config
import pandas as pd
from pyMABED import detect_events
from pyMABED import build_event_browser
import relevant_topic_detection
import random
import pickle
import tqdm

def get_details(tweets, crowded_places):
    tweets = data_prep(tweets)
    file_name = 'related_tweets.csv'
    places_events_tweets = {}

    for place in crowded_places:
        print('Getting details for place {}')
        related_tweets = spatial_selection(place, tweets)
        related_tweets = temporal_selection(place, related_tweets)
        related_tweets.to_csv(Config.results + file_name, sep='\t', encoding='utf-8')

        run_pyMABED(file_name)

        top_k_topics = pickle.load(open(Config.pyMABED_args_detect_event['o'], 'rb'))

        related_events = filter_topics(top_k_topics, place)

        related_events_with_tweets = add_tweets(related_events, related_tweets)

        places_events_tweets[str(place)] = related_events_with_tweets

    return places_events_tweets


def data_prep(tweets):
    tweets[['gridx', 'gridy']] = pd.DataFrame(tweets['grid'].tolist(), index=tweets.index)
    tweets.drop('grid', axis=1, inplace=True)
    tweets[['gridx', 'gridy']] = tweets[['gridx', 'gridy']].astype(int)
    return tweets


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


def run_pyMABED(file_name):

    Config.pyMABED_args_detect_event['i'] = Config.results + file_name

    detect_events.main(Config.pyMABED_args_detect_event)
    build_event_browser.main(Config.pyMABED_args_built_ui)
    print('pyMABED is done.')

def filter_topics(top_k_topics, place):
    related_events = []
    for topic in top_k_topics.events:
        related_topic = relevant_topic_detection.check_topic_relevant(topic, place, top_k_topics)
        if related_topic is None:
            continue
        related_events.append(related_topic)
    return related_events

def add_tweets(related_events, related_tweets):
    for event in related_events:
        example_tweets = search_tweets(event, related_tweets)

        event['tweets'] = example_tweets
    return related_events

def search_tweets(event, related_tweets):
    example_tweets = []
    for index, row in related_tweets.iterrows():
        matches = sum(row['text'].lower().count(word) for word in event['rel_words'])

        if matches >= 3:
            example_tweets.append((row['screen_name'], row['text']))

    return get_random_sample(example_tweets)

def get_random_sample(example_tweets):
    final_tweets = []
    for i in range(10):
        final_tweets.append(random.choice(example_tweets))
    return final_tweets
