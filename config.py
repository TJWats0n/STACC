class Config:


    data_type = 'static' #'stream' or 'static'

    data = 'raw_data/'
    prep_data = 'data/'
    helper_files = 'helper_files/'
    results = 'results/'


    spam_filter = ["#Hiring", "#hiring", "hiring", "Hiring", "#job",
                    "Just posted a photo", "Just posted a video", "Foto appena pubblicata", "Good morning, New York!",
                    "Cleared:", "Updated:", "UV", "Incident on", "Construction on",
                   "New York", "NY", "new york", "ny", "nyc"]

    map_size = 24
    interval = 360  # in minutes
    city = 'manhattan'
    grid_box = [-74.09523, 40.720721, -73.832932, 40.898463]
    sliding_window = 20 # how many days
    radius = 3
    corpus_size_factor = 4 # include tweets in corpus from now-(corpus_size_factor*interval) until now

    num_topics = 10
    overlap = 0.7

    pyMABED_args_detect_event = {
        'i': None,
        'k': 10,
        'sw': 'pyMABED/stopwords/twitter_en.txt',
        'sep': '\t',
        'o': helper_files + '/top_events.p',
        'maf': 10,
        'mrf': 0.4,
        'tsl': 30,
        'p': 10,
        't': 0.6,
        's': 0.6
    }

    pyMABED_args_built_ui = {
        'i': results + '/pyMABED_visu.p',
        'o': '../results/ui'
    }

    # Twitter API keys
    API_keys = {
        'jk': {
            'ckey': '9sjG3qaG7QTl1I0BvVXztMWHB',
            'csecret': 'piB2RnsQvOe99BZqFFTJawwkhEqrgop8XhJeQ1a9ihHeBBmmXS',
            'atoken': '4353511715-75aoTofgrOYguk5MRLmUrbn1n6iVBVmwduHGPpW',
            'asecret': '4qEllHZzXRZUdwf7Q42GV8FISO0z2O6w47Bpm67z6kCao',
        }
    }
