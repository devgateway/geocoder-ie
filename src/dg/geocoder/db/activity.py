import logging

import psycopg2
import psycopg2.extras

from dg.geocoder.db.db import open, close

logger = logging.getLogger()


def get_activity_by_id(activity_id):
    conn = None
    try:
        conn = open()
        sql_select = "SELECT * FROM ACTIVITY where id=%s"
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(sql_select, (activity_id,))

        activity = cur.fetchone()
        cur.close()

        return activity
    except Exception as error:
        logger.info(error)
    finally:
        close(conn)
