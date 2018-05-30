from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
from real_time_config import RTConfig
from cloudant.client import Cloudant
from requests.adapters import HTTPAdapter
import json


class listener(StreamListener):

    def on_data (self, data):
        while True:
            try:
                database.create_document(json.loads(data))
            except Exception as e:
                print('failed ondata,',str(e))
                init_db()
                time.sleep(5)
            break

    def on_error (self, status):
        print(status)
        return False


def init_db():
    print('Init DB')
    global database
    httpAdapter = HTTPAdapter(pool_connections=15, pool_maxsize=100)
    client = Cloudant(RTConfig.cloudant_cred['username'],
                      RTConfig.cloudant_cred['password'],
                      url=RTConfig.cloudant_cred['url'],
                      connect=True,
                      adapter=httpAdapter)

    database = client['streamed_tweets']


def main():
    init_db()
    while True:
        for k,v in RTConfig.keys.items():
            print('switching to {}'.format(k))
            
            auth = OAuthHandler(v['ckey'], v['csecret'])
            auth.set_access_token(v['atoken'], v['asecret'])
            try:
                twitterStream = Stream (auth, listener())
                nyc_box = [-74.09523,40.720721,-73.832932,40.898463]
                twitterStream.filter(locations=nyc_box)
            except:
                pass

if __name__ == '__main__':
    main()
