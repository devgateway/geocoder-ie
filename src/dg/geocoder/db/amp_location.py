import logging

import psycopg2
import psycopg2.extras

from dg.geocoder.db.db import open, close

logger = logging.getLogger()


def clean_amp_locations():
    logger.info("Clean AMP_LOCATION table")
    conn = open()
    sql = 'DELETE FROM AMP_LOCATION'
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()
    close(conn)


def save_amp_locations(locations):
    conn = None
    try:
        conn = open()
        sql = """INSERT INTO AMP_LOCATION (ID, AMP_LOCATION_ID, NAME, ADMIN_LEVEL_CODE, DESCRIPTION, 
            GEO_CODE, GS_LAT, GS_LONG) 
            VALUES (NEXTVAL('amp_location_id_seq'), %s, %s, %s, %s, %s, %s, %s)"""
        cur = conn.cursor()

        for loc in locations:
            data = (loc["amp_location_id"], loc["name"], loc["admin_level_code"], loc["description"],
                    loc["geo_code"], loc["gs_lat"], loc["gs_long"])
            cur.execute(sql, data)

        conn.commit()
        cur.close()
    except Exception as error:
        logger.info(error)
        raise
    finally:
        close(conn)


def get_amp_location_by_id(location_id):
    conn = None
    try:
        conn = open()
        sql_select = """SELECT * FROM AMP_LOCATION where id = %s """
        cur = conn.cursor()
        data = (location_id,)
        cur.execute(sql_select, data)

        row = cur.fetchone()
        cur.close()

        return row

    except Exception as error:
        logger.info(error)
        raise
    finally:
        close(conn)


def get_amp_locations():
    conn = None
    try:
        conn = open()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        sql_select = """SELECT * FROM AMP_LOCATION"""
        cursor.execute(sql_select)

        results = cursor.fetchall()
        cursor.close()

        return results

    except Exception as error:
        logger.info(error)
        raise
    finally:
        close(conn)
