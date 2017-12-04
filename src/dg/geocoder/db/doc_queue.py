import logging

import psycopg2

from dg.geocoder.constants import ST_PROCESSED
from dg.geocoder.db.db import open, close

logger = logging.getLogger()


def add_job_to_queue(file_name, file_type, country_iso, state='PENDING'):
    conn = None
    try:
        conn = open()
        sql = """INSERT INTO QUEUE (QUEUE_TYPE,ID, FILE_NAME, FILE_TYPE, STATE, CREATE_DATE, COUNTRY_ISO) VALUES 
        ('DOC_QUEUE',NEXTVAL('hibernate_sequence'),%s,%s, %s, NOW(), %s )"""
        cur = conn.cursor()
        data = (file_name, file_type, state, country_iso)
        cur.execute(sql, data)
        conn.commit()
        cur.close()
    except Exception as error:
        logger.info(error)
        raise
    finally:
        close(conn)


def delete_all_docs_from_queue():
    conn = open()
    sql_1 = "DELETE FROM EXTRACT WHERE GEOCODING_ID IN (SELECT ID FROM GEOCODING WHERE DOCUMENT_ID in (SELECT ID FROM DOC_QUEUE WHERE STATE IN ('PENDING','ERROR','PROCESSING')))"
    sql_2 = "DELETE FROM GEOCODING WHERE DOCUMENT_ID IN (SELECT ID FROM DOC_QUEUE)"
    sql_3 = "DELETE FROM ACTIVITY WHERE DOCUMENT_ID IN (SELECT ID FROM DOC_QUEUE)"
    sql_4 = "DELETE FROM DOC_QUEUE"
    cur = conn.cursor()
    cur.execute(sql_1)
    cur.execute(sql_2)
    cur.execute(sql_3)
    cur.execute(sql_4)
    rowcount = cur.rowcount

    conn.commit()
    cur.close()
    close(conn)
    return rowcount > 0


def delete_doc_from_queue(doc_id):
    conn = open()
    sql_1 = "DELETE FROM EXTRACT WHERE GEOCODING_ID IN (SELECT ID FROM GEOCODING WHERE DOCUMENT_ID=%s)"
    sql_2 = "DELETE FROM GEOCODING WHERE DOCUMENT_ID=%s"
    sql_3 = "DELETE FROM ACTIVITY WHERE DOCUMENT_ID=%s"
    sql_4 = "DELETE FROM QUEUE WHERE ID = %s"
    cur = conn.cursor()
    cur.execute(sql_1, (doc_id,))
    cur.execute(sql_2, (doc_id,))
    cur.execute(sql_3, (doc_id,))
    cur.execute(sql_4, (doc_id,))
    rowcount = cur.rowcount

    conn.commit()
    cur.close()
    close(conn)
    return rowcount > 0


def get_queue_list(page=1, limit=10, states=None, doc_type=None):
    conn = None
    try:
        if page == 0:
            page = 1

        conn = open()
        offset = (limit * int(page)) - limit
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        sql_count = "SELECT COUNT(*) FROM QUEUE WHERE 1=1 "
        sql_select = """SELECT q.*, a.identifier FROM QUEUE  q left join activity a on q.activity_id=a.id WHERE 1=1 """
        data = ()

        if states is not None:
            sql_count = sql_count + " AND STATE in %s "
            sql_select = sql_select + """AND STATE in %s """
            data = data + (tuple(states),)

        cur.execute(sql_count, data)
        count = cur.fetchone().get("count")

        sql_select = sql_select + " ORDER BY CREATE_DATE DESC OFFSET %s LIMIT %s "

        data = data + (offset, limit)
        cur.execute(sql_select, data)

        results = cur.fetchall()

        cur.close()

        return {'count': count, 'rows': results, 'limit': limit}

    except Exception as error:
        logger.info(error)
        raise

    finally:
        close(conn)


def get_queue_by_id(doc_id):
    conn = None
    try:
        conn = open()
        sql_select = """SELECT * FROM QUEUE where id = %s """
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        data = (doc_id,)
        cur.execute(sql_select, data)
        row = cur.fetchone()
        cur.close()

        return row

    except Exception as error:
        logger.info(error)
        raise
    finally:
        close(conn)


def update_queue_status(doc_id, status, message=''):
    conn = None
    try:
        conn = open()
        sql = "UPDATE QUEUE SET STATE=%s ,MESSAGE=%s "

        if status == ST_PROCESSED:
            sql = sql + ",PROCESSED_DATE=NOW() "

        sql = sql + "WHERE ID = %s "
        cur = conn.cursor()
        data = (status, message, doc_id)
        cur.execute(sql, data)
        conn.commit()
        cur.close()
    except Exception as error:
        logger.info(error)
        raise
    finally:
        close(conn)
