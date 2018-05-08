from config import Config
import datetime as dt

# ================================ helper functions ============================================

def poi_metrics(crowded_place):
    end = crowded_place[0]
    start = end - dt.timedelta(minutes=Config.interval)
    duration = Config.interval
    return start, duration

def event_metrics(events, event, dt_str_format):
    start = dt.datetime.strptime(str(events.corpus.to_date(event[1][0])), dt_str_format)
    end = dt.datetime.strptime(str(events.corpus.to_date(event[1][1])), dt_str_format)
    duration = end - start
    duration = duration.total_seconds() / 60
    return start, end, duration

# ================================ main functions ============================================

def calc_overlap(events, crowded_place):
    dt_str_format = '%Y-%m-%d %H:%M:%S'
    relevant_events = []

    for event in events.events:

        event_start, event_end, event_duration = event_metrics(events, event, dt_str_format)
        poi_start, poi_duration = poi_metrics(crowded_place)

        delta = event_end - poi_start

        if delta.total_seconds() > 0:

            #80% of the event must take place in PoI
            overlap = delta.total_seconds() / event_duration

            #The event must take place 80% of the PoI time
            overlap_alt = delta.total_seconds() / poi_duration

        if overlap > Config.overlap:
            related_words = []
            for related_word, weight in event[3]:
                related_words.append(related_word)

            relevant_events.append({'magnitude': event[0],
                                    'start_end': (event_start.strftime(dt_str_format), event_end.strftime(dt_str_format)),
                                    'main_words': event[2],
                                    'rel_words': related_words})

        return relevant_events






