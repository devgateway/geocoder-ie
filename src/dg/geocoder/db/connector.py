import psycopg2


def open():
    try:
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect('dbname=geocoder user=postgres password=admin')
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print("Wasn't able to connect")
        raise


def close(conn):
    if conn is not None:
        try:
            conn.close()
        except (Exception, psycopg2.Error) as error:
            print('error when closing connection')


def save_geocoded_sentence(activity_id, sentence, entities=[], geocoding=[]):
    insert_sentence = """INSERT INTO SENTENCE (id,activity_id,sentence) values (nextval('global_id_seq'),%s,%s) RETURNING ID"""
    insert_entity = "INSERT INTO entity (id, sentence_id, name) VALUES (nextval('global_id_seq'),%s,%s) RETURNING ID"
    insert_coding = "INSERT INTO public.autogeocoding(id, name, entity_id) VALUES (nextval('global_id_seq'), %s, %s) RETURNING ID"

    data = (activity_id, sentence)
    conn = open()
    cur = conn.cursor()
    # execute the INSERT statement
    cur.execute(insert_sentence, data)
    # get the generated id back
    sentence_id = cur.fetchone()[0]

    for name in entities:
        data = (sentence_id, name)
        cur.execute(insert_entity, data)

    # commit the changes to the database
    conn.commit()
    # close communication with the database
    cur.close()
