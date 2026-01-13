--
-- PostgreSQL database dump
--

\restrict ZfsBi4WEK4WLncQpBZNWheZt1IfOwfsfU86Qpylv8VNqRAgYfXtLg57kmLHSU3z

-- Dumped from database version 17.5 (Debian 17.5-1)
-- Dumped by pg_dump version 18.1 (Debian 18.1-1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: portfolio_user
--

-- *not* creating schema, since initdb creates it


ALTER SCHEMA public OWNER TO portfolio_user;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: Projects; Type: TABLE; Schema: public; Owner: portfolio_user
--

CREATE TABLE public."Projects" (
    id integer NOT NULL,
    title character varying(200) NOT NULL,
    description text NOT NULL,
    technologies json,
    github_url character varying(300),
    live_url character varying(300),
    image_url character varying(300),
    featured boolean,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone,
    screenshots json DEFAULT '[]'::json
);


ALTER TABLE public."Projects" OWNER TO portfolio_user;

--
-- Name: Projects_id_seq; Type: SEQUENCE; Schema: public; Owner: portfolio_user
--

CREATE SEQUENCE public."Projects_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Projects_id_seq" OWNER TO portfolio_user;

--
-- Name: Projects_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: portfolio_user
--

ALTER SEQUENCE public."Projects_id_seq" OWNED BY public."Projects".id;


--
-- Name: blog_posts; Type: TABLE; Schema: public; Owner: portfolio_user
--

CREATE TABLE public.blog_posts (
    id integer NOT NULL,
    title character varying(200) NOT NULL,
    content text NOT NULL,
    slug character varying(200),
    published boolean,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.blog_posts OWNER TO portfolio_user;

--
-- Name: blog_posts_id_seq; Type: SEQUENCE; Schema: public; Owner: portfolio_user
--

CREATE SEQUENCE public.blog_posts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.blog_posts_id_seq OWNER TO portfolio_user;

--
-- Name: blog_posts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: portfolio_user
--

ALTER SEQUENCE public.blog_posts_id_seq OWNED BY public.blog_posts.id;


--
-- Name: skills; Type: TABLE; Schema: public; Owner: portfolio_user
--

CREATE TABLE public.skills (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    category character varying(50),
    level integer DEFAULT 3,
    icon_url character varying(300),
    description text,
    display_order integer DEFAULT 0,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT skills_level_check CHECK (((level >= 1) AND (level <= 5)))
);


ALTER TABLE public.skills OWNER TO portfolio_user;

--
-- Name: skills_id_seq; Type: SEQUENCE; Schema: public; Owner: portfolio_user
--

CREATE SEQUENCE public.skills_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.skills_id_seq OWNER TO portfolio_user;

--
-- Name: skills_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: portfolio_user
--

ALTER SEQUENCE public.skills_id_seq OWNED BY public.skills.id;


--
-- Name: Projects id; Type: DEFAULT; Schema: public; Owner: portfolio_user
--

ALTER TABLE ONLY public."Projects" ALTER COLUMN id SET DEFAULT nextval('public."Projects_id_seq"'::regclass);


--
-- Name: blog_posts id; Type: DEFAULT; Schema: public; Owner: portfolio_user
--

ALTER TABLE ONLY public.blog_posts ALTER COLUMN id SET DEFAULT nextval('public.blog_posts_id_seq'::regclass);


--
-- Name: skills id; Type: DEFAULT; Schema: public; Owner: portfolio_user
--

ALTER TABLE ONLY public.skills ALTER COLUMN id SET DEFAULT nextval('public.skills_id_seq'::regclass);


--
-- Data for Name: Projects; Type: TABLE DATA; Schema: public; Owner: portfolio_user
--

COPY public."Projects" (id, title, description, technologies, github_url, live_url, image_url, featured, created_at, updated_at, screenshots) FROM stdin;
46	Todo	Un project todo standart , uniquement coté front-end avec localstorage	["React", "daisyUI"]	https://github.com/geek-Konate/Todo-react-		\N	f	2026-01-12 23:10:27.797156+01	\N	["http://localhost:8000/uploads/screenshots/3168e3ba-6935-489d-aef4-9b23b38621d9.png", "http://localhost:8000/uploads/screenshots/5577f585-b9c3-49a6-8e71-8f836ec1863f.png"]
47	Api	Mon projet d'entraînement a l'API	[]	https://github.com/geek-Konate/Project-D-entrainement		\N	f	2026-01-12 23:19:35.274485+01	\N	["http://localhost:8000/uploads/screenshots/4629e803-c9f8-45e8-a42c-fa7a28add282.png", "http://localhost:8000/uploads/screenshots/71badee7-1010-4629-8083-cc8c618426e8.png", "http://localhost:8000/uploads/screenshots/afa1d423-7c1c-43dc-ba07-4fd47d75464c.png"]
\.


--
-- Data for Name: blog_posts; Type: TABLE DATA; Schema: public; Owner: portfolio_user
--

COPY public.blog_posts (id, title, content, slug, published, created_at) FROM stdin;
\.


--
-- Data for Name: skills; Type: TABLE DATA; Schema: public; Owner: portfolio_user
--

COPY public.skills (id, name, category, level, icon_url, description, display_order, created_at) FROM stdin;
1	React	frontend	4	\N	Développement d'interfaces utilisateur modernes avec hooks et context	1	2026-01-03 11:21:05.676333+01
2	TypeScript	frontend	3	\N	Typage statique pour applications JavaScript robustes	2	2026-01-03 11:21:05.676333+01
3	Tailwind CSS	frontend	4	\N	Framework CSS utility-first pour des designs rapides	3	2026-01-03 11:21:05.676333+01
4	Python	backend	5	\N	Développement backend, scripts et automatisation	4	2026-01-03 11:21:05.676333+01
5	FastAPI	backend	4	\N	Framework web asynchrone pour APIs modernes	5	2026-01-03 11:21:05.676333+01
6	Flask	backend	3	\N	Micro-framework web Python simple et flexible	6	2026-01-03 11:21:05.676333+01
7	PostgreSQL	database	4	\N	Base de données relationnelle avancée	7	2026-01-03 11:21:05.676333+01
8	SQLAlchemy	database	3	\N	ORM Python pour les bases de données	8	2026-01-03 11:21:05.676333+01
9	Docker	devops	3	\N	Conteneurisation d'applications	9	2026-01-03 11:21:05.676333+01
10	Git	tools	4	\N	Système de contrôle de version distribué	10	2026-01-03 11:21:05.676333+01
11	GitHub	tools	4	\N	Plateforme de collaboration et hébergement de code	11	2026-01-03 11:21:05.676333+01
12	Linux	tools	3	\N	Administration système et ligne de commande	12	2026-01-03 11:21:05.676333+01
13	Figma	design	3	\N	Design d'interfaces et prototypage	13	2026-01-03 11:21:05.676333+01
14	VSCode	tools	4	\N	Éditeur de code avec extensions	14	2026-01-03 11:21:05.676333+01
\.


--
-- Name: Projects_id_seq; Type: SEQUENCE SET; Schema: public; Owner: portfolio_user
--

SELECT pg_catalog.setval('public."Projects_id_seq"', 47, true);


--
-- Name: blog_posts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: portfolio_user
--

SELECT pg_catalog.setval('public.blog_posts_id_seq', 1, false);


--
-- Name: skills_id_seq; Type: SEQUENCE SET; Schema: public; Owner: portfolio_user
--

SELECT pg_catalog.setval('public.skills_id_seq', 14, true);


--
-- Name: Projects Projects_pkey; Type: CONSTRAINT; Schema: public; Owner: portfolio_user
--

ALTER TABLE ONLY public."Projects"
    ADD CONSTRAINT "Projects_pkey" PRIMARY KEY (id);


--
-- Name: blog_posts blog_posts_pkey; Type: CONSTRAINT; Schema: public; Owner: portfolio_user
--

ALTER TABLE ONLY public.blog_posts
    ADD CONSTRAINT blog_posts_pkey PRIMARY KEY (id);


--
-- Name: skills skills_pkey; Type: CONSTRAINT; Schema: public; Owner: portfolio_user
--

ALTER TABLE ONLY public.skills
    ADD CONSTRAINT skills_pkey PRIMARY KEY (id);


--
-- Name: ix_Projects_id; Type: INDEX; Schema: public; Owner: portfolio_user
--

CREATE INDEX "ix_Projects_id" ON public."Projects" USING btree (id);


--
-- Name: ix_blog_posts_id; Type: INDEX; Schema: public; Owner: portfolio_user
--

CREATE INDEX ix_blog_posts_id ON public.blog_posts USING btree (id);


--
-- Name: ix_blog_posts_slug; Type: INDEX; Schema: public; Owner: portfolio_user
--

CREATE UNIQUE INDEX ix_blog_posts_slug ON public.blog_posts USING btree (slug);


--
-- PostgreSQL database dump complete
--

\unrestrict ZfsBi4WEK4WLncQpBZNWheZt1IfOwfsfU86Qpylv8VNqRAgYfXtLg57kmLHSU3z

