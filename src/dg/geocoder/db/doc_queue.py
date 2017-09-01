import logging

from dg.geocoder.db.db import open, close

logger = logging.getLogger()


def save_doc(file_name, file_type, country_iso):
    conn = None
    try:
        conn = open()
        sql = """INSERT INTO DOC_QUEUE (ID, FILE_NAME, TYPE, STATE, CREATE_DATE, COUNTRY_ISO) VALUES (NEXTVAL('DOC_ID_SEQ'),%s,%s, 'PENDING', NOW(), %s )"""
        cur = conn.cursor()
        data = (file_name, file_type, country_iso)
        cur.execute(sql, data)
        conn.commit()
        cur.close()
    except Exception as error:
        logger.info(error)
        raise
    finally:
        close(conn)


def delete_doc_from_queue(id):
    conn = open()
    sql = """DELETE FROM DOC_QUEUE WHERE ID = %s"""
    cur = conn.cursor()
    cur.execute(sql, (id,))
    rowcount = cur.rowcount
    conn.commit()
    cur.close()
    close(conn)
    return rowcount > 0


def get_docs(page=1, limit=10, state=None, doc_type=None):
    conn = None
    try:
        if page == 0:
            page = 1

        conn = open()
        offset = (limit * int(page)) - limit
        cur = conn.cursor()

        sql_count = "SELECT COUNT(*) FROM DOC_QUEUE WHERE 1=1 "
        sql_select = """SELECT * FROM DOC_QUEUE WHERE 1=1 """
        data = ()

        if state is not None:
            if state == 'PENDING':
                sql_count = sql_count + " AND STATE != %s "
                sql_select = sql_select + """AND STATE != %s """
                data = data + ('PROCESSED',)
            else:
                sql_count = sql_count + " AND STATE = %s "
                sql_select = sql_select + """AND STATE = %s """
                data = data + (state,)

        cur.execute(sql_count, data)
        count = cur.fetchone()[0]

        sql_select = sql_select + " ORDER BY CREATE_DATE DESC OFFSET %s LIMIT %s "

        data = data + (offset, limit)
        cur.execute(sql_select, data)

        results = [(c) for c in cur]
        cur.close()

        return {'count': count, 'rows': results, 'limit': limit}

    except Exception as error:
        logger.info(error)
        raise

    finally:
        close(conn)


def get_document_by_id(doc_id):
    conn = None
    try:
        conn = open()
        sql_select = """SELECT * FROM DOC_QUEUE where id = %s """
        cur = conn.cursor()
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


def update_doc_status(id, status, message=''):
    conn = None
    try:
        conn = open()
        sql = """UPDATE DOC_QUEUE SET STATE=%s ,MESSAGE=%s, PROCESSED_DATE=NOW() WHERE ID = %s"""
        cur = conn.cursor()
        data = (status, message, id)
        cur.execute(sql, data)
        conn.commit()
        cur.close()
    except Exception as error:
        logger.info(error)
        raise
    finally:
        close(conn)
