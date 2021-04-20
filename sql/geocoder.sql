

CREATE SEQUENCE public.hibernate_sequence
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 7344
  CACHE 1;
ALTER TABLE public.hibernate_sequence
  OWNER TO postgres;



CREATE SEQUENCE corpora_id_seq
    START WITH 1012266
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


-- Table: public.corpora

-- DROP TABLE public.corpora;

CREATE TABLE public.corpora
(
  id bigint NOT NULL,
  sentence text,
  category character varying(100),
  file character varying(500),
  ref_id bigint,
  CONSTRAINT corpora_pk PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.corpora
  OWNER TO postgres;


SELECT setval('corpora_id_seq', (SELECT MAX(id) +1 FROM corpora));


-- Table: public.activity

-- DROP TABLE public.activity;

CREATE TABLE public.activity
(
  id bigint NOT NULL,
  identifier character varying(255),
  CONSTRAINT activity_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.activity
  OWNER TO postgres;


CREATE INDEX idxxffomfb0jkw84hhhqqwyc3mq
  ON public.activity
  USING btree
  (identifier COLLATE pg_catalog."default");




-- Table: public.queue

-- DROP TABLE public.queue;

CREATE TABLE public.queue
(
  queue_type character varying(31) NOT NULL,
  id bigint NOT NULL,
  create_date timestamp without time zone,
  message character varying(500),
  processed_date timestamp without time zone,
  state character varying(255),
  country_iso character varying(255),
  file_name character varying(255),
  file_type character varying(255),
  out_file character varying(255),
  activity_id bigint,
  CONSTRAINT queue_pkey PRIMARY KEY (id),
  CONSTRAINT fkkwa4qv22vmj6kvlo629ywg2ih FOREIGN KEY (activity_id)
      REFERENCES public.activity (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.queue
  OWNER TO postgres;

-- Index: public.idx5c69i3wujd85b8m5hx7jmi0tl

-- DROP INDEX public.idx5c69i3wujd85b8m5hx7jmi0tl;

CREATE INDEX idx5c69i3wujd85b8m5hx7jmi0tl
  ON public.queue
  USING btree
  (state COLLATE pg_catalog."default");

-- Index: public.idxbwtdx4od3f898l689gy5m3ae2

-- DROP INDEX public.idxbwtdx4od3f898l689gy5m3ae2;

CREATE INDEX idxbwtdx4od3f898l689gy5m3ae2
  ON public.queue
  USING btree
  (activity_id);

-- Index: public.idxjyijs2kwgb5lklfip2bf3bvr0

-- DROP INDEX public.idxjyijs2kwgb5lklfip2bf3bvr0;

CREATE INDEX idxjyijs2kwgb5lklfip2bf3bvr0
  ON public.queue
  USING btree
  (queue_type COLLATE pg_catalog."default");



CREATE TABLE public.geocoding
(
  id bigint NOT NULL,
  activity_id bigint,
  admin_code1 character varying(255),
  admin_code2 character varying(255),
  admin_code3 character varying(255),
  admin_code4 character varying(255),
  admin_name1 character varying(255),
  admin_name2 character varying(255),
  admin_name3 character varying(255),
  admin_name4 character varying(255),
  continentcode character varying(255),
  country_code character varying(255),
  country_name character varying(255),
  fcl character varying(255),
  fclname character varying(255),
  fcode character varying(255),
  fcodename character varying(255),
  geoname_id integer,
  lat double precision,
  lng double precision,
  name character varying(255),
  population character varying(255),
  toponym_name character varying(255),
  queue_id bigint,
  CONSTRAINT geocoding_pkey PRIMARY KEY (id),
  CONSTRAINT fkp9h8j84vkvf12fqd7ortdk2du FOREIGN KEY (queue_id)
      REFERENCES public.queue (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.geocoding
  OWNER TO postgres;


  -- Table: public."extract"

-- DROP TABLE public."extract";

CREATE TABLE public."extract"
(
  id bigint NOT NULL,
  entities character varying(500),
  entity character varying(500),
  file_name character varying(500),
  text text,
  geocoding_id bigint,
  --location_id bigint,
  queue_id bigint,
  location_id bigint,
  CONSTRAINT extract_pkey PRIMARY KEY (id),
  CONSTRAINT fk26fwawxc2na6xk46iatswri0w FOREIGN KEY (geocoding_id)
      REFERENCES public.geocoding (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  --CONSTRAINT fk741kklp394i5g2dtd5dj0llj3 FOREIGN KEY (location_id)
    --  REFERENCES public.location (id) MATCH SIMPLE
     -- ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT fk7fphqpqfy51xe6tps9suh497v FOREIGN KEY (queue_id)
      REFERENCES public.queue (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public."extract"
  OWNER TO postgres;

-- Index: public.idxija4h3o7cah01wc4cqbd31i9o

-- DROP INDEX public.idxija4h3o7cah01wc4cqbd31i9o;

CREATE INDEX idxija4h3o7cah01wc4cqbd31i9o
  ON public."extract"
  USING btree
  (geocoding_id);
