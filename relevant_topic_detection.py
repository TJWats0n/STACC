from config import Config
import datetime as dt


def check_topic_relevant(topic, crowded_place, top_k_topics):
    event_start, event_end, event_duration, poi_start, poi_duration = start_end_points(topic, crowded_place, top_k_topics)
    overlap = calc_overlap(event_start, event_end, event_duration, poi_start, poi_duration)

    if overlap > Config.overlap:
        related_words = []
        for related_word, weight in topic[3]:
            related_words.append(related_word)

        # make searching related words easier for later
        related_words.append(topic[2])

        relevant_topic = ({'magnitude': topic[0],
                                'start_end': (event_start.strftime('%Y-%m-%d %H:%M:%S'),
                                              event_end.strftime('%Y-%m-%d %H:%M:%S')),
                                'main_words': topic[2],
                                'rel_words': related_words})

        return relevant_topic
    return None


def calc_overlap(event_start, event_end, event_duration, poi_start, poi_duration):
    delta = event_end - poi_start
    overlap = 0
    if delta.total_seconds() > 0:
        check = event_start - poi_start
        if check.total_seconds() > 0:
            overlap = 1
        else:
            #80% of the event must take place in PoI
            overlap = ((delta.total_seconds()/60) / event_duration)

            #The event must take place 80% of the PoI time
            overlap_alt = (delta.total_seconds()/60 / poi_duration)

    return overlap


def start_end_points(topic, crowded_place, top_k_topics):
    event_start, event_end, event_duration = event_metrics(top_k_topics, topic)
    poi_start, poi_duration = poi_metrics(crowded_place)
    return event_start, event_end, event_duration, poi_start, poi_duration

def poi_metrics(crowded_place):
    end = crowded_place[0]
    start = end - dt.timedelta(minutes=Config.interval)
    duration = Config.interval
    return start, duration


def event_metrics(top_k_topics, event):
    start = dt.datetime.strptime(str(top_k_topics.corpus.to_date(event[1][0])), '%Y-%m-%d %H:%M:%S')
    end = dt.datetime.strptime(str(top_k_topics.corpus.to_date(event[1][1])), '%Y-%m-%d %H:%M:%S')
    duration = end - start
    duration = int(duration.total_seconds() / 60)
    return start, end, duration


