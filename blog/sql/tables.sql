CREATE TABLE IF NOT EXISTS users
(
  id serial unique,
  first_name character varying(32) NOT NULL,
  last_name character varying(32) NOT NULL,
  email character varying(256) NOT NULL,
  password character varying(256) NOT NULL,
  is_superuser boolean NOT NULL DEFAULT 'FALSE',
  is_deleted boolean NOT NULL DEFAULT 'FALSE',
  CONSTRAINT user_pkey PRIMARY KEY (id),
  CONSTRAINT user_login_key UNIQUE (email)
);

CREATE TABLE IF NOT EXISTS posts
(
    id serial unique,
    user_id integer NOT NULL,
    title character varying(64) NOT NULL,
    content character varying(2048) NOT NULL,
    posted_at date default now() NOT NULL,

    CONSTRAINT post_pkey PRIMARY KEY (id),
    CONSTRAINT user_post_fkey FOREIGN KEY (user_id)
        REFERENCES users (id) MATCH SIMPLE
        ON UPDATE NO ACTION ON DELETE CASCADE

);

CREATE TABLE IF NOT EXISTS permissions
(
  id integer NOT NULL,
  user_id integer NOT NULL,
  perm_name character varying(64) NOT NULL,
  CONSTRAINT permission_pkey PRIMARY KEY (id),
  CONSTRAINT user_permission_fkey FOREIGN KEY (user_id)
      REFERENCES users (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE
);

