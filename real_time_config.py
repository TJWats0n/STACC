class RTConfig:
    #Database credentials
    cloudant_cred = {
        "username": "your_cred_here",
        "password": "your_cred_here",
        "host": "your_cred_here",
        "port": 443,
        "url": "your_cred_here"
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
            'ckey': 'your_key_here',
            'csecret': 'your_key_here',
            'atoken': 'your_key_here',
            'asecret': 'your_key_here',
        }
    }