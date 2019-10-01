import logging

from dg.geocoder.db.corpora import save_sentences
from dg.geocoder.readers.json_reader import JsonReader

logger = logging.getLogger()


def load_activities_corpora(json):
    for activity in json:
        reader = JsonReader(activity)
        for s, p in reader.split():
            logger.info("breaking activity " + activity["amp_id"])
            save_sentences(p, [s], activity["amp_id"])
