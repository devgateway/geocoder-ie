from dg.geocoder.db.db import open, close


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
        sql = """INSERT INTO CORPORA (id,file, sentence,category) values (nextval('global_id_seq'),%s,%s ,null)"""

        cur = conn.cursor()
        for s in sentences:
            data = (file, s)
            cur.execute(sql, data)

        conn.commit()
        cur.close()
    except Exception as error:
        print(error)
        pass
    finally:
        close(conn)
