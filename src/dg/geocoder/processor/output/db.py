import logging

from dg.geocoder.db.db import open, close
from dg.geocoder.db.geocode import save_geocoding, save_extract_text, save_activity

logger = logging.getLogger()


# Save an activity imported from command line
def persist_activity(results, activity, doc_id):
    identifier = activity.get_identifier()
    title = activity.get_title()
    description = activity.get_description()
    country = activity.get_recipient_country_code()
    activity_id = save_activity(identifier, title, description, country, doc_id)
    geocoding = [(data['geocoding'], data['texts']) for (l, data) in results if data.get('geocoding')]
    persist_geocoding(geocoding, doc_id, activity_id)


def persist_geocoding(results, activity_id, job_id, document_id):
    geocoding_list = [(data['geocoding'], data['texts']) for (l, data) in results if data.get('geocoding')]
    for geocoding in geocoding_list:
        try:
            conn = open()
            location_id, geocoding_id = save_geocoding(geocoding[0], job_id, activity_id, document_id, conn=conn)
            for text in geocoding[1]:
                save_extract_text(text.get('text'), geocoding_id, ', '.join(text.get('entities')), conn=conn)

            conn.commit()
        except Exception as error:
            conn.cancel()
            logger.info(error)
            raise
        finally:
            close(conn)
    return None
