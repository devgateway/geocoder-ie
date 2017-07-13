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
