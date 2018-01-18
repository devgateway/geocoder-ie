import logging

from dg.geocoder.db.db import open, close

logger = logging.getLogger()


def clean():
    conn = open()
    sql = 'DELETE FROM CORPORA'
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()
    close(conn)


def save_sentences(file, sentences):
    conn = None
    try:
        conn = open()
        sql = """INSERT INTO CORPORA (ID,FILE, SENTENCE,CATEGORY) VALUES (NEXTVAL('corpora_id_seq'),%s,%s ,NULL )"""
        cur = conn.cursor()
        for s in sentences:
            data = (file, s)
            cur.execute(sql, data)

        conn.commit()
        cur.close()
    except Exception as error:
        logger.info(error)
        raise
    finally:
        close(conn)


def delete_sentence(corpora_id):
    conn = open()
    sql = """DELETE FROM CORPORA WHERE ID = %s"""
    cur = conn.cursor()
    cur.execute(sql, (corpora_id,))
    rowcount = cur.rowcount
    conn.commit()
    cur.close()
    close(conn)
    return rowcount > 0


def set_category(corpora_id, category):
    rowcount = 0
    conn = open()
    try:
        sql = """UPDATE CORPORA SET CATEGORY=%s WHERE ID = %s"""
        cur = conn.cursor()
        cur.execute(sql, (category, corpora_id))
        rowcount = cur.rowcount
        conn.commit()
        cur.close()
    except Exception as e:
        logger.info('error %s', e)
        raise

    finally:
        close(conn)
        return rowcount > 0


def get_sentence_by_id(sentence_id):
    conn = None
    try:
        conn = open()
        sql_select = """SELECT * FROM CORPORA where id = %s """
        cur = conn.cursor()
        data = (sentence_id,)
        cur.execute(sql_select, data)

        row = cur.fetchone()
        cur.close()

        return row

    except Exception as error:
        logger.info(error)
        raise
    finally:
        close(conn)


def get_sentences(page=1, limit=50, query=None, category=None, document=None):
    conn = None
    try:
        if page == 0:
            page = 1

        conn = open()
        offset = (limit * int(page)) - limit
        cur = conn.cursor()

        sql_count = "SELECT COUNT(*) FROM CORPORA WHERE 1=1 "
        sql_select = """SELECT * FROM CORPORA WHERE 1=1 """
        data = ()

        if query is not None:
            sql_count = sql_count + " AND SENTENCE ilike %s "
            sql_select = sql_select + """AND SENTENCE ilike %s """
            data = data + ('%%%s%%' % query,)

        if category is not None:
            sql_count = sql_count + " AND CATEGORY = %s "
            sql_select = sql_select + """AND CATEGORY = %s """
            data = data + (category,)

        if document is not None:
            sql_count = sql_count + " AND FILE like %s "
            sql_select = sql_select + """ AND FILE like %s """
            data = data + ('%%%s' % document,)

        cur.execute(sql_count, data)
        count = cur.fetchone()[0]

        sql_select = sql_select + " ORDER BY ID  OFFSET %s LIMIT %s "

        data = data + (offset, limit)
        cur.execute(sql_select, data)

        results = [c for c in cur]
        cur.close()

        return {'count': count, 'rows': results, 'limit': limit}

    except Exception as error:
        logger.info(error)
        raise
    finally:
        close(conn)


def get_doc_list():
    conn = None
    try:
        conn = open()
        cur = conn.cursor()
        sql_select = """SELECT distinct(file) FROM CORPORA order by file"""
        cur.execute(sql_select)
        results = [(c[0]) for c in cur]
        cur.close()
        return results
    except Exception as error:
        logger.info(error)
        raise
    finally:
        close(conn)
