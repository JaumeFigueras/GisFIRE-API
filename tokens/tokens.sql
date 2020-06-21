CREATE TABLE public.tokens
(
   id bigserial,
   username varchar(50),
   token varchar(64),
   admin boolean,
   valid_until timestamp with time zone,
   ts timestamp with time zone DEFAULT (now() at time zone 'utc'),
   CONSTRAINT pk_tokens PRIMARY KEY (id),
   CONSTRAINT uq_tokens_username UNIQUE (username)
)
WITH (
  OIDS = FALSE
)
;
ALTER TABLE public.xdde_requests
  OWNER TO gisfireuser
;

CREATE TABLE public.access
(
   id bigserial,
   token_id bigint,
   ip inet,
   ts timestamp with time zone DEFAULT (now() at time zone 'utc'),
   CONSTRAINT pk_access PRIMARY KEY (id),
   CONSTRAINT fk_access_tokens FOREIGN KEY (token_id) REFERENCES public.tokens (id)
)
WITH (
  OIDS = FALSE
)
;
ALTER TABLE public.xdde_requests
  OWNER TO gisfireuser
;
