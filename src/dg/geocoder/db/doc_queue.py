from dg.geocoder.db.db import open, close


def save_doc(file_name, file_type):
    conn = None
    try:
        conn = open()
        sql = """INSERT INTO DOC_QUEUE (ID, FILE_NAME, TYPE, STATE, CREATE_DATE) VALUES (NEXTVAL('DOC_ID_SEQ'),%s,%s, 'PENDING', NOW() )"""
        cur = conn.cursor()
        data = (file_name, file_type)
        cur.execute(sql, data)
        conn.commit()
        cur.close()
    except Exception as error:
        print(error)
        pass
    finally:
        close(conn)


def get_docs(page=1, limit=50, state=None, doc_type=None):
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
            sql_count = sql_count + " AND STATE = %s "
            sql_select = sql_select + """AND STATE = %s """
            data = data + (state,)

        if doc_type is not None:
            sql_count = sql_count + " AND TYPE = %s "
            sql_select = sql_select + """AND TYPE = %s """
            data = data + (doc_type,)

        cur.execute(sql_count, data)
        count = cur.fetchone()[0]

        sql_select = sql_select + " ORDER BY ID  OFFSET %s LIMIT %s "

        data = data + (offset, limit)
        cur.execute(sql_select, data)

        results = [(c) for c in cur]
        cur.close()

        return {'count': count, 'rows': results, 'limit': limit}

    except Exception as error:
        print(error)
        pass
    finally:
        close(conn)

