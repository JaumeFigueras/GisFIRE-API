CREATE TABLE public.user_token
(
   id bigserial,
   username varchar NOT NULL,
   token varchar(64) NOT NULL,
   is_admin boolean DEFAULT FALSE,
   valid_until timestamp with time zone DEFAULT NULL,
   ts timestamp with time zone DEFAULT (now() at time zone 'utc'),
   CONSTRAINT pk_user_token PRIMARY KEY (id),
   CONSTRAINT uq_user_token_username UNIQUE (username)
)
WITH (
  OIDS = FALSE
)
;
ALTER TABLE public.user_token
  OWNER TO gisfireuser
;
GRANT ALL ON public.user_access
  TO remotegisfireuser
;

CREATE TABLE public.user_access
(
   id bigserial,
   user_id bigint,
   ip inet NOT NULL,
   url varchar NOT NULL,
   method varchar NOT NULL,
   params varchar DEFAULT NULL,
   result_code int,
   ts timestamp with time zone DEFAULT (now() at time zone 'utc'),
   CONSTRAINT pk_user_access PRIMARY KEY (id),
   CONSTRAINT fk_user_access_user_token FOREIGN KEY (user_id) REFERENCES public.user_token (id)
)
WITH (
  OIDS = FALSE
)
;
ALTER TABLE public.user_access
  OWNER TO gisfireuser
;
GRANT ALL ON public.user_access
  TO remotegisfireuser
;