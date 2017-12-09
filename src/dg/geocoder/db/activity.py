import logging

from dg.geocoder.db.db import open, close

logger = logging.getLogger()


def activity_to_dic(activity):
    return {"id": activity[0],
            "identifier": activity[1],
            "xml": activity[2]}


def get_activity_by_id(activity_id):
    conn = None
    try:
        conn = open()
        sql_select = """SELECT * FROM ACTIVITY where id = %s """
        cur = conn.cursor()
        data = (activity_id,)
        cur.execute(sql_select, data)

        activity = cur.fetchone()
        cur.close()

        return activity_to_dic(activity)

    except Exception as error:
        logger.info(error)
    finally:
        close(conn)
