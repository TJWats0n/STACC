from flask import Flask, jsonify, render_template
import pickle
from config import Config
import pandas as pd
from collections import OrderedDict
from flask_cors import CORS


app = Flask(__name__, static_folder='static')
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/v1.0/places', methods=['GET'])
def get_places():
    return jsonify(places_helper())


@app.route('/api/v1.0/events/<place_time>/<int:place_x>/<int:place_y>/<int:place_amount>', methods=['GET'])
def get_events_for_place(place_time, place_x, place_y, place_amount):
    key = (pd.Timestamp(place_time), (float(place_x), float(place_y)), place_amount)
    return jsonify(events_helper(key))


@app.route('/api/v1.0/tweets/<place_time>/<int:place_x>/<int:place_y>/<int:place_amount>/<int:event_id>', methods=['GET'])
def get_tweets(place_time, place_x, place_y, place_amount, event_id):
    key = (pd.Timestamp(place_time), (place_x, place_y), place_amount)
    return jsonify(tweets_helper(key, event_id))

def tweets_helper(key, event_id):
    data = load_file()

    try:
        return data[key][event_id]['tweets']
    except IndexError:
        return {'message': 'There are only less than {} events.'.format(event_id)} #construct json with key 'message' --> should be displayed in browser
    except KeyError:
        return {'message': 'There is no crowded place corresponding to {}'.format(key)}
    except TypeError:
        return {'message': 'There is no file to load crowded places from.'}


def places_helper():
    data = load_file()

    places = OrderedDict()
    try:
        for index, key in enumerate(sorted(data.keys())):
            places[str(index)] = {'timestamp': key[0],
                                  'x': int(key[1][0]),
                                  'y': int(key[1][1]),
                                  'tweet_amount': str(key[2])}
        return places

    except AttributeError:
        return {'message': 'There is no file to load crowded places from.'}


def events_helper(key):
    data = load_file()

    events = {}
    try:
        for index, event in enumerate(data[key]):
            events[str(index)] = {'start_end': [event['start_end'][0], event['start_end'][1]],
                                 'main_words': event['main_words'],
                                 'rel_words': event['rel_words']}

        return events
    except KeyError:
        return {'message': 'There is no crowded place corresponding to {}'.format(key)}
    except TypeError:
        return {'message': 'There is no file to load crowded places from.'}

def load_file():
    try:
        with open(Config.results + 'master_object.p', 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        return


if __name__ == "__main__":
    app.run(debug=True)