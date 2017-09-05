import logging

from dg.geocoder.db.db import open, close

logger = logging.getLogger()


def save_doc(file_name, file_type, country_iso):
    conn = None
    try:
        conn = open()
        sql = """INSERT INTO DOC_QUEUE (ID, FILE_NAME, TYPE, STATE, CREATE_DATE, COUNTRY_ISO) VALUES 
        (NEXTVAL('GLOBAL_ID_SEQ'),%s,%s, 'PENDING', NOW(), %s )"""
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


def delete_doc_from_queue(doc_id):
    conn = open()
    sql_1 = "DELETE FROM EXTRACT WHERE GEOCODING_ID IN (SELECT ID FROM GEOCODING WHERE DOCUMENT_ID=%s)"
    sql_2 = "DELETE FROM GEOCODING WHERE DOCUMENT_ID=%s"
    sql_3 = "DELETE FROM ACTIVITY WHERE DOCUMENT_ID=%s"
    sql_4 = "DELETE FROM DOC_QUEUE WHERE ID = %s"
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


def get_docs(page=1, limit=10, states=None, doc_type=None):
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

        if states is not None:
            sql_count = sql_count + " AND STATE in %s "
            sql_select = sql_select + """AND STATE in %s """
            data = data + (tuple(states),)

        cur.execute(sql_count, data)
        count = cur.fetchone()[0]

        sql_select = sql_select + " ORDER BY CREATE_DATE DESC OFFSET %s LIMIT %s "

        data = data + (offset, limit)
        cur.execute(sql_select, data)

        results = [{'id': c[0],
                    'file_name': c[1],
                    'type': c[2],
                    'state': c[3],
                    'create_date': c[4],
                    'processed_date': c[5],
                    'country_iso': c[6],
                    'message': c[7]

                    } for c in cur]
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

        return {'id': row[0],
                    'file_name': row[1],
                    'type': row[2],
                    'state': row[3],
                    'create_date': row[4],
                    'processed_date': row[5],
                    'country_iso': row[6],
                    'message': row[7]

                    }

    except Exception as error:
        logger.info(error)
        raise
    finally:
        close(conn)


def update_doc_status(doc_id, status, message=''):
    conn = None
    try:
        conn = open()
        sql = """UPDATE DOC_QUEUE SET STATE=%s ,MESSAGE=%s, PROCESSED_DATE=NOW() WHERE ID = %s"""
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
