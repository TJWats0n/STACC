#execution file for heroku, now with capital P
heroku ps:scale web=1 worker=1
web: gunicorn server:app #working for gunicorn 
worker: python real_time_handler.py