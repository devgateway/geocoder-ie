



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


CREATE TABLE public.corpora
(
  id bigint NOT NULL,
  sentence text,
  category character varying(100),
  file character varying(500),
  CONSTRAINT corpora_pk PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.corpora
  OWNER TO postgres;