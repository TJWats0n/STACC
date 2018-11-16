from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
from real_time_config import RTConfig
from datetime import datetime
import os
import csv


class Listener(StreamListener):
    current_date = datetime.strptime('2000-01-01', '%Y-%m-%d').date()
    date_for_file = '{}-{}-{}'.format(current_date.year, current_date.month, current_date.day)
    file_per_day = 0
    filename = ''

    def on_data (self, data):
        while True:
            try:
                now = datetime.now().date()
                if Listener.current_date!= now:
                    Listener.date_for_file = '{)-{}-{}'.format(now.year, now.month, now.day)
                    Listener.file_per_day = 0
                    Listener.filename = 'tweets_{}_{}.csv'.format(Listener.date_for_file, Listener.file_per_day)

                if os.path.getsize('raw_data/{}'.format(Listener.filename)) > 80000000: #80MB
                    Listener.file_per_day =+ 1
                    Listener.filename = 'tweets_{}_{}.csv'.format(Listener.date_for_file, Listener.file_per_day)

                with open(Listener.filename, 'a') as file:
                    csvwriter = csv.writer(file)
                    csvwriter.writerow(data)

            except Exception as e:
                print('failed ondata,',str(e))
                time.sleep(5)
            break

    def on_error (self, status):
        print(status)
        return False



def main():

    while True:
        for k,v in RTConfig.keys.items():
            print('switching to {}'.format(k))
            
            auth = OAuthHandler(v['ckey'], v['csecret'])
            auth.set_access_token(v['atoken'], v['asecret'])
            try:
                twitterstream = Stream(auth, Listener())
                nyc_box = [-74.09523,40.720721,-73.832932,40.898463]
                twitterstream.filter(locations=nyc_box)
            except:
                pass

if __name__ == '__main__':
    main()
