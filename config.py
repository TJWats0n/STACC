class Config:


    data_type = 'static' #'stream' or 'static'
    data = 'raw_data/'
    prep_data = 'data/'
    results = 'results/'


    spam_filter = ["#Hiring", "#hiring", "hiring", "Hiring", "#job",
                    "Just posted a photo", "Just posted a video", "Foto appena pubblicata", "Good morning, New York!",
                    "Cleared:", "Updated:", "UV", "Incident on", "Construction on"]

    map_size = 24
    interval = 360  # in minutes
    city = 'manhattan'
    sliding_window = 20 # how many days
    radius = 3
    corpus_size_factor = 4

    num_topics = 10
    overlap = 0.7

    pyMABED_args_detect_event = {
        'i': None,
        'k': 10,
        'sw': 'pyMABED/stopwords/twitter_en.txt',
        'sep': '\t',
        'o': 'other_files/top_events.p',
        'maf': 10,
        'mrf': 0.4,
        'tsl': 30,
        'p': 10,
        't': 0.6,
        's': 0.6
    }

    pyMABED_args_built_ui = {
        'i': 'results/pyMABED_visu.p',
        'o': '../results/ui'
    }
