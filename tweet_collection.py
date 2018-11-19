from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from datetime import datetime
import os, csv, time
from config import Config


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
                    Listener.current_date = now
                    Listener.date_for_file = '{}-{}-{}'.format(now.year, now.month, now.day)
                    Listener.file_per_day = 0
                    Listener.filename = 'tweets_{}_{}.csv'.format(Listener.date_for_file, Listener.file_per_day)

                with open('{}/{}'.format(Config.data, Listener.filename), 'a+') as file:
                    csvwriter = csv.writer(file)
                    csvwriter.writerow([data])

                if os.path.getsize('{}/{}'.format(Config.data, Listener.filename)) >= 80000000: #80MB
                    Listener.file_per_day += 1
                    Listener.filename = 'tweets_{}_{}.csv'.format(Listener.date_for_file, Listener.file_per_day)

            except Exception as e:
                print('failed ondata,',str(e))
                time.sleep(5)
            break

    def on_error (self, status):
        print(status)
        return False



def main():

    while True:
        for k,v in Config.API_keys.items():
            print('switching to {}'.format(k))
            
            auth = OAuthHandler(v['ckey'], v['csecret'])
            auth.set_access_token(v['atoken'], v['asecret'])
            try:
                twitterstream = Stream(auth, Listener())
                twitterstream.filter(locations=Config.grid_box)
            except:
                pass

if __name__ == '__main__':
    main()
