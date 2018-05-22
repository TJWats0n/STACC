from flask import Flask, jsonify
import pickle
from config import Config
import pandas as pd


app = Flask(__name__)


@app.route('/')
def index():
    return 'hello world'

@app.route('/api/v1.0/places', methods=['GET'])
def get_places():
    return jsonify(places_helper())


@app.route('/api/v1.0/events/<place_id>', methods=['GET'])
def get_events_for_place(place_id):
    places = places_helper()
    return jsonify(events_helper(places, place_id))




@app.route('/api/v1.0/tweets/<place_id>/<event_id>', methods=['GET'])
def get_tweets_for_event(place_id, event_id):
    places = places_helper()
    events = events_helper(places, place_id)
    return jsonify({str(index): tweet for index, tweet in enumerate(events[event_id]['tweets'])})

def places_helper():
    with open(Config.results + 'master_object.p', 'rb') as file:
        data = pickle.load(file)

    places = {}
    for index, key in enumerate(data.keys()):
        places[str(index)] = {'timestamp': key[0],
                              'x': key[1][0],
                              'y': key[1][1],
                              'tweet_amount': str(key[2])}
    return places

def events_helper(places, place_id):
    key = (pd.Timestamp(places[place_id]['timestamp']), (float(places[place_id]['x']), float(places[place_id]['y'])),
           int(places[place_id]['tweet_amount']))
    with open(Config.results + 'master_object.p', 'rb') as file:
        data = pickle.load(file)

    events = {}
    for index, event in enumerate(data[key]):
        events[str(index)] = {'start_end': [event['start_end'][0], event['start_end'][1]],
                             'main_words': event['main_words'],
                             'rel_words': event['rel_words']}

    return events


if __name__ == "__main__":
    app.run(debug=True)