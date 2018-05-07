class Config:


    data_type = 'static' #'stream' or 'static'

    data = 'data/'
    city = 'manhattan'

    spam_filter = ["#Hiring", "#hiring", "hiring", "Hiring", "#job",
                    "Just posted a photo", "Just posted a video", "Good morning, New York!",
                    "Cleared:", "Updated:", "UV", "Incident on", "Construction on"]

    map_size = 10
    interval = 360  # in minutes
