CREATE TABLE public.products
(
    name character varying NOT NULL,
    price integer NOT NULL,
    id serial,
    PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS public.products
    OWNER to postgres;