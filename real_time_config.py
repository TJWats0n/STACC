class RTConfig:
    #Database credentials
    cloudant_cred = {
        "username": "0a9dac16-96d4-4ea9-b41a-62bcd51de0f5-bluemix",
        "password": "c8490e7b530803b38044e6fcb9b92903aa178a22f9cd9f214f1d372d5e5993a3",
        "host": "0a9dac16-96d4-4ea9-b41a-62bcd51de0f5-bluemix.cloudant.com",
        "port": 443,
        "url": "https://0a9dac16-96d4-4ea9-b41a-62bcd51de0f5-bluemix:c8490e7b530803b38044e6fcb9b92903aa178a22f9cd9f214f1d372d5e5993a3@0a9dac16-96d4-4ea9-b41a-62bcd51de0f5-bluemix.cloudant.com"
    }

    selector = {
        "created_at": {
            "$gte": "",
            "$lte": ""
        },
        "$not": {
            "geo": None
        }
    }

    fields = ["user.screen_name", "text", "created_at", "geo.coordinates"]

    #Twitter API keys
    keys = {
        'jk': {
            'ckey': 'xdACHwFupBPsFDGmsF6H7HKNU',
            'csecret': '6ZBryD8NrtGSWiLDfe2XYmj1f8jzEXkpzgSkEjKqbhxTlUtBIQ',
            'atoken': '2865752009-r766x9fKZx0kBY4MCAEuIE5T4EYmkjvEYc77n1q',
            'asecret': 'EXVhwGJjsPGnmDS7TWZ2ICu7vilJeYIpNgQjMhaF9YicA',
        }
    }