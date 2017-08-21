



CREATE SEQUENCE public.global_id_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1012266
  CACHE 1;
ALTER TABLE public.global_id_seq
  OWNER TO postgres;



CREATE SEQUENCE doc_id_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 14
  CACHE 1;

CREATE TABLE doc_queue
(
  id bigint NOT NULL,
  file_name character varying(500),
  type character varying(50),
  state character varying(50),
  create_date timestamp without time zone,
  processed_date timestamp without time zone,
  country_iso character varying(50),
  CONSTRAINT doc_queue_pk PRIMARY KEY (id)
);

CREATE TABLE activity
(
  id bigint NOT NULL,
  name character varying(500),
  description character varying(500),
  country_iso character varying(250),
  doc_id bigint,
  CONSTRAINT activity_pk PRIMARY KEY (id),
  CONSTRAINT fk_doc_queue_activity_id FOREIGN KEY (id)
      REFERENCES doc_queue (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE geocoding
(
  id bigint NOT NULL,
  geoname_id bigint NOT NULL,
  toponym_name character varying(250),
  name character varying(250),
  lat character varying(250),
  lng character varying(250),
  country_code character varying(250),
  country_name character varying(250),
  fcl character varying(250),
  fcode character varying(250),
  fclname character varying(250),
  fcodename character varying(250),
  population character varying(250),
  continentcode character varying(250),
  admin_code_1 character varying(250),
  admin_name_1 character varying(250),
  admin_code_2 character varying(250),
  admin_name_2 character varying(250),
  admin_code_3 character varying(250),
  admin_name_3 character varying(250),
  admin_code_4 character varying(250),
  admin_name_4 character varying(250),
  document_id bigint,
  activity_id bigint,
  CONSTRAINT geocoding_pk PRIMARY KEY (id),
  CONSTRAINT fk_geocoding_activity FOREIGN KEY (activity_id)
      REFERENCES activity (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT fk_geocoding_document FOREIGN KEY (document_id)
      REFERENCES doc_queue (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE "extract"
(
  id bigint NOT NULL,
  text character varying(250),
  entities character varying(250),
  geocoding_id bigint,
  CONSTRAINT extract_pk PRIMARY KEY (id),
  CONSTRAINT fk_extract_geocoding FOREIGN KEY (geocoding_id)
      REFERENCES geocoding (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
);


CREATE TABLE public.corpora
(
  id bigint NOT NULL,
  sentence text,
  category character varying(100),
  file character varying(500),
  CONSTRAINT corpora_pk PRIMARY KEY (id)
);
