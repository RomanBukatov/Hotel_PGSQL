--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

-- Started on 2025-05-01 16:38:27

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 230 (class 1259 OID 17051)
-- Name: bookingoccupants; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.bookingoccupants (
    bookingid integer NOT NULL,
    guestid integer NOT NULL,
    isadditionalplace boolean DEFAULT false NOT NULL,
    includesbreakfast boolean DEFAULT false NOT NULL,
    includesdinner boolean DEFAULT false NOT NULL
);


ALTER TABLE public.bookingoccupants OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 17032)
-- Name: bookings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.bookings (
    bookingid integer NOT NULL,
    clientid integer NOT NULL,
    bookingdate date NOT NULL,
    checkindate date NOT NULL,
    checkoutdate date NOT NULL,
    categoryid integer NOT NULL,
    status text DEFAULT 'Pending'::text NOT NULL
);


ALTER TABLE public.bookings OWNER TO postgres;

--
-- TOC entry 228 (class 1259 OID 17031)
-- Name: bookings_bookingid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.bookings_bookingid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.bookings_bookingid_seq OWNER TO postgres;

--
-- TOC entry 5017 (class 0 OID 0)
-- Dependencies: 228
-- Name: bookings_bookingid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.bookings_bookingid_seq OWNED BY public.bookings.bookingid;


--
-- TOC entry 224 (class 1259 OID 16995)
-- Name: features; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.features (
    featureid integer NOT NULL,
    name text NOT NULL
);


ALTER TABLE public.features OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 16994)
-- Name: features_featureid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.features_featureid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.features_featureid_seq OWNER TO postgres;

--
-- TOC entry 5018 (class 0 OID 0)
-- Dependencies: 223
-- Name: features_featureid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.features_featureid_seq OWNED BY public.features.featureid;


--
-- TOC entry 218 (class 1259 OID 16957)
-- Name: guests; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.guests (
    guestid integer NOT NULL,
    lastname text NOT NULL,
    firstname text NOT NULL,
    middlename text,
    dateofbirth date,
    placeofbirth text,
    passportseries text,
    passportnumber text,
    passportissuedate date,
    passportissuedby text,
    address text,
    phone text,
    email text,
    discountcardnumber text
);


ALTER TABLE public.guests OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 16956)
-- Name: guests_guestid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.guests_guestid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.guests_guestid_seq OWNER TO postgres;

--
-- TOC entry 5019 (class 0 OID 0)
-- Dependencies: 217
-- Name: guests_guestid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.guests_guestid_seq OWNED BY public.guests.guestid;


--
-- TOC entry 220 (class 1259 OID 16968)
-- Name: roomcategories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.roomcategories (
    categoryid integer NOT NULL,
    name text NOT NULL,
    description text,
    basepricepernight real NOT NULL
);


ALTER TABLE public.roomcategories OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16967)
-- Name: roomcategories_categoryid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.roomcategories_categoryid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.roomcategories_categoryid_seq OWNER TO postgres;

--
-- TOC entry 5020 (class 0 OID 0)
-- Dependencies: 219
-- Name: roomcategories_categoryid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.roomcategories_categoryid_seq OWNED BY public.roomcategories.categoryid;


--
-- TOC entry 225 (class 1259 OID 17005)
-- Name: roomcategoryfeatures; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.roomcategoryfeatures (
    categoryid integer NOT NULL,
    featureid integer NOT NULL
);


ALTER TABLE public.roomcategoryfeatures OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 16979)
-- Name: rooms; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rooms (
    roomid integer NOT NULL,
    roomnumber text NOT NULL,
    categoryid integer NOT NULL
);


ALTER TABLE public.rooms OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 16978)
-- Name: rooms_roomid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.rooms_roomid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.rooms_roomid_seq OWNER TO postgres;

--
-- TOC entry 5021 (class 0 OID 0)
-- Dependencies: 221
-- Name: rooms_roomid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.rooms_roomid_seq OWNED BY public.rooms.roomid;


--
-- TOC entry 227 (class 1259 OID 17021)
-- Name: services; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.services (
    serviceid integer NOT NULL,
    name text NOT NULL,
    description text,
    baseprice real,
    priceunit text
);


ALTER TABLE public.services OWNER TO postgres;

--
-- TOC entry 226 (class 1259 OID 17020)
-- Name: services_serviceid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.services_serviceid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.services_serviceid_seq OWNER TO postgres;

--
-- TOC entry 5022 (class 0 OID 0)
-- Dependencies: 226
-- Name: services_serviceid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.services_serviceid_seq OWNED BY public.services.serviceid;


--
-- TOC entry 235 (class 1259 OID 17105)
-- Name: serviceusage; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.serviceusage (
    serviceusageid integer NOT NULL,
    stayid integer NOT NULL,
    serviceid integer NOT NULL,
    dateofusage date NOT NULL,
    timeofusage time without time zone,
    quantity real DEFAULT 1 NOT NULL,
    priceperunit real NOT NULL,
    totalcost real NOT NULL
);


ALTER TABLE public.serviceusage OWNER TO postgres;

--
-- TOC entry 234 (class 1259 OID 17104)
-- Name: serviceusage_serviceusageid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.serviceusage_serviceusageid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.serviceusage_serviceusageid_seq OWNER TO postgres;

--
-- TOC entry 5023 (class 0 OID 0)
-- Dependencies: 234
-- Name: serviceusage_serviceusageid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.serviceusage_serviceusageid_seq OWNED BY public.serviceusage.serviceusageid;


--
-- TOC entry 233 (class 1259 OID 17088)
-- Name: stayoccupants; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.stayoccupants (
    stayid integer NOT NULL,
    guestid integer NOT NULL,
    isprimaryguest boolean DEFAULT false NOT NULL
);


ALTER TABLE public.stayoccupants OWNER TO postgres;

--
-- TOC entry 232 (class 1259 OID 17070)
-- Name: stays; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.stays (
    stayid integer NOT NULL,
    roomid integer NOT NULL,
    checkindate date NOT NULL,
    plannedcheckoutdate date NOT NULL,
    actualcheckoutdate date,
    bookingid integer,
    autonumber text
);


ALTER TABLE public.stays OWNER TO postgres;

--
-- TOC entry 231 (class 1259 OID 17069)
-- Name: stays_stayid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.stays_stayid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.stays_stayid_seq OWNER TO postgres;

--
-- TOC entry 5024 (class 0 OID 0)
-- Dependencies: 231
-- Name: stays_stayid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.stays_stayid_seq OWNED BY public.stays.stayid;


--
-- TOC entry 4794 (class 2604 OID 17035)
-- Name: bookings bookingid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bookings ALTER COLUMN bookingid SET DEFAULT nextval('public.bookings_bookingid_seq'::regclass);


--
-- TOC entry 4792 (class 2604 OID 16998)
-- Name: features featureid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.features ALTER COLUMN featureid SET DEFAULT nextval('public.features_featureid_seq'::regclass);


--
-- TOC entry 4789 (class 2604 OID 16960)
-- Name: guests guestid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.guests ALTER COLUMN guestid SET DEFAULT nextval('public.guests_guestid_seq'::regclass);


--
-- TOC entry 4790 (class 2604 OID 16971)
-- Name: roomcategories categoryid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roomcategories ALTER COLUMN categoryid SET DEFAULT nextval('public.roomcategories_categoryid_seq'::regclass);


--
-- TOC entry 4791 (class 2604 OID 16982)
-- Name: rooms roomid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms ALTER COLUMN roomid SET DEFAULT nextval('public.rooms_roomid_seq'::regclass);


--
-- TOC entry 4793 (class 2604 OID 17024)
-- Name: services serviceid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.services ALTER COLUMN serviceid SET DEFAULT nextval('public.services_serviceid_seq'::regclass);


--
-- TOC entry 4801 (class 2604 OID 17108)
-- Name: serviceusage serviceusageid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.serviceusage ALTER COLUMN serviceusageid SET DEFAULT nextval('public.serviceusage_serviceusageid_seq'::regclass);


--
-- TOC entry 4799 (class 2604 OID 17073)
-- Name: stays stayid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stays ALTER COLUMN stayid SET DEFAULT nextval('public.stays_stayid_seq'::regclass);


--
-- TOC entry 5006 (class 0 OID 17051)
-- Dependencies: 230
-- Data for Name: bookingoccupants; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 5005 (class 0 OID 17032)
-- Dependencies: 229
-- Data for Name: bookings; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 5000 (class 0 OID 16995)
-- Dependencies: 224
-- Data for Name: features; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.features VALUES (1, 'Wi-Fi');
INSERT INTO public.features VALUES (3, 'Джакузи');
INSERT INTO public.features VALUES (4, 'Сейф');
INSERT INTO public.features VALUES (5, 'Вид на море');
INSERT INTO public.features VALUES (6, 'Рабочая зона');
INSERT INTO public.features VALUES (7, 'Умный дом');


--
-- TOC entry 4994 (class 0 OID 16957)
-- Dependencies: 218
-- Data for Name: guests; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.guests VALUES (1, 'Иванов', 'Иван', 'Иванович', '1990-01-01', 'Москва', '1234', '567890', '2010-01-01', 'ОВД Москвы', 'ул. Пушкина, д. 1', '+79991234567', 'ivanov@example.com', '123456');
INSERT INTO public.guests VALUES (3, 'Смирнов', 'Олег', 'Васильевич', '1988-07-15', 'Краснодар', '0306', '987654', '2013-08-20', 'УФМС России по Краснодарскому краю', 'г. Краснодар, ул. Красная, д. 15, кв. 10', '+79182345678', 'smirnov@mail.ru', '67890');
INSERT INTO public.guests VALUES (4, 'Николаева', 'Мария', 'Ивановна', '1992-03-25', 'Волгоград', '1807', '456789', '2016-04-15', 'УФМС России по Волгоградской области', 'г. Волгоград, ул. Мира, д. 25, кв. 20', '+79172345678', 'nikolaeva@mail.ru', '78901');
INSERT INTO public.guests VALUES (5, 'Кузнецов', 'Сергей', 'Николаевич', '1975-11-10', 'Омск', '5208', '234567', '2010-12-05', 'УФМС России по Омской области', 'г. Омск, ул. Ленина, д. 35, кв. 30', '+79132345678', 'kuznetsov@mail.ru', '89012');
INSERT INTO public.guests VALUES (6, 'Федорова', 'Екатерина', 'Алексеевна', '1990-05-20', 'Ростов-на-Дону', '6109', '345678', '2014-06-15', 'УФМС России по Ростовской области', 'г. Ростов-на-Дону, ул. Большая Садовая, д. 45, кв. 40', '+79182345678', 'fedorova@mail.ru', '90123');
INSERT INTO public.guests VALUES (2, 'Букатов', 'Роман', 'Викторович', '2006-08-27', 'Абакан', '1234', '543424', '2006-12-23', 'мной', 'улица пушкина дом колотушкиноэ', '+7983760949', 'roman_voprosik@mail.ru', '412312314124');


--
-- TOC entry 4996 (class 0 OID 16968)
-- Dependencies: 220
-- Data for Name: roomcategories; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.roomcategories VALUES (1, 'Стандарт', 'Стандартный номер', 2000);
INSERT INTO public.roomcategories VALUES (2, 'Премиум', 'Премиум номер с панорамным видом', 7000);
INSERT INTO public.roomcategories VALUES (3, 'Студио', 'Номер-студия с кухонной зоной', 3500);
INSERT INTO public.roomcategories VALUES (4, 'Апартаменты', 'Просторные апартаменты с кухней', 6000);
INSERT INTO public.roomcategories VALUES (5, 'Эконом', 'Бюджетный номер для экономных путешественников', 1500);
INSERT INTO public.roomcategories VALUES (6, 'Президентский', 'Роскошный номер высшей категории', 15000);


--
-- TOC entry 5001 (class 0 OID 17005)
-- Dependencies: 225
-- Data for Name: roomcategoryfeatures; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.roomcategoryfeatures VALUES (1, 1);
INSERT INTO public.roomcategoryfeatures VALUES (2, 3);
INSERT INTO public.roomcategoryfeatures VALUES (2, 5);
INSERT INTO public.roomcategoryfeatures VALUES (3, 6);
INSERT INTO public.roomcategoryfeatures VALUES (4, 4);
INSERT INTO public.roomcategoryfeatures VALUES (6, 7);
INSERT INTO public.roomcategoryfeatures VALUES (6, 3);


--
-- TOC entry 4998 (class 0 OID 16979)
-- Dependencies: 222
-- Data for Name: rooms; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.rooms VALUES (1, '101', 1);
INSERT INTO public.rooms VALUES (2, '601', 2);
INSERT INTO public.rooms VALUES (3, '602', 2);
INSERT INTO public.rooms VALUES (4, '701', 3);
INSERT INTO public.rooms VALUES (5, '702', 4);
INSERT INTO public.rooms VALUES (6, '801', 6);


--
-- TOC entry 5003 (class 0 OID 17021)
-- Dependencies: 227
-- Data for Name: services; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.services VALUES (1, 'Завтрак', 'Континентальный завтрак', 500, 'сутки');
INSERT INTO public.services VALUES (3, 'Спа-процедуры', 'Комплекс спа-процедур для лица и тела', 3500, 'сеанс');
INSERT INTO public.services VALUES (4, 'Трансфер', 'Трансфер из/в аэропорт', 1500, 'поездка');
INSERT INTO public.services VALUES (5, 'Сауна', 'Посещение сауны (1 час)', 1000, 'час');
INSERT INTO public.services VALUES (6, 'Мини-бар', 'Пополнение мини-бара в номере', 800, 'заказ');
INSERT INTO public.services VALUES (7, 'Экскурсия', 'Индивидуальная экскурсия по городу', 2500, 'экскурсия');


--
-- TOC entry 5011 (class 0 OID 17105)
-- Dependencies: 235
-- Data for Name: serviceusage; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 5009 (class 0 OID 17088)
-- Dependencies: 233
-- Data for Name: stayoccupants; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 5008 (class 0 OID 17070)
-- Dependencies: 232
-- Data for Name: stays; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 5025 (class 0 OID 0)
-- Dependencies: 228
-- Name: bookings_bookingid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.bookings_bookingid_seq', 1, true);


--
-- TOC entry 5026 (class 0 OID 0)
-- Dependencies: 223
-- Name: features_featureid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.features_featureid_seq', 7, true);


--
-- TOC entry 5027 (class 0 OID 0)
-- Dependencies: 217
-- Name: guests_guestid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.guests_guestid_seq', 7, true);


--
-- TOC entry 5028 (class 0 OID 0)
-- Dependencies: 219
-- Name: roomcategories_categoryid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.roomcategories_categoryid_seq', 6, true);


--
-- TOC entry 5029 (class 0 OID 0)
-- Dependencies: 221
-- Name: rooms_roomid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.rooms_roomid_seq', 6, true);


--
-- TOC entry 5030 (class 0 OID 0)
-- Dependencies: 226
-- Name: services_serviceid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.services_serviceid_seq', 7, true);


--
-- TOC entry 5031 (class 0 OID 0)
-- Dependencies: 234
-- Name: serviceusage_serviceusageid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.serviceusage_serviceusageid_seq', 1, true);


--
-- TOC entry 5032 (class 0 OID 0)
-- Dependencies: 231
-- Name: stays_stayid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.stays_stayid_seq', 1, true);


--
-- TOC entry 4828 (class 2606 OID 17058)
-- Name: bookingoccupants bookingoccupants_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bookingoccupants
    ADD CONSTRAINT bookingoccupants_pkey PRIMARY KEY (bookingid, guestid);


--
-- TOC entry 4826 (class 2606 OID 17040)
-- Name: bookings bookings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bookings
    ADD CONSTRAINT bookings_pkey PRIMARY KEY (bookingid);


--
-- TOC entry 4816 (class 2606 OID 17004)
-- Name: features features_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.features
    ADD CONSTRAINT features_name_key UNIQUE (name);


--
-- TOC entry 4818 (class 2606 OID 17002)
-- Name: features features_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.features
    ADD CONSTRAINT features_pkey PRIMARY KEY (featureid);


--
-- TOC entry 4804 (class 2606 OID 16966)
-- Name: guests guests_discountcardnumber_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.guests
    ADD CONSTRAINT guests_discountcardnumber_key UNIQUE (discountcardnumber);


--
-- TOC entry 4806 (class 2606 OID 16964)
-- Name: guests guests_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.guests
    ADD CONSTRAINT guests_pkey PRIMARY KEY (guestid);


--
-- TOC entry 4808 (class 2606 OID 16977)
-- Name: roomcategories roomcategories_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roomcategories
    ADD CONSTRAINT roomcategories_name_key UNIQUE (name);


--
-- TOC entry 4810 (class 2606 OID 16975)
-- Name: roomcategories roomcategories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roomcategories
    ADD CONSTRAINT roomcategories_pkey PRIMARY KEY (categoryid);


--
-- TOC entry 4820 (class 2606 OID 17009)
-- Name: roomcategoryfeatures roomcategoryfeatures_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roomcategoryfeatures
    ADD CONSTRAINT roomcategoryfeatures_pkey PRIMARY KEY (categoryid, featureid);


--
-- TOC entry 4812 (class 2606 OID 16986)
-- Name: rooms rooms_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms
    ADD CONSTRAINT rooms_pkey PRIMARY KEY (roomid);


--
-- TOC entry 4814 (class 2606 OID 16988)
-- Name: rooms rooms_roomnumber_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms
    ADD CONSTRAINT rooms_roomnumber_key UNIQUE (roomnumber);


--
-- TOC entry 4822 (class 2606 OID 17030)
-- Name: services services_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.services
    ADD CONSTRAINT services_name_key UNIQUE (name);


--
-- TOC entry 4824 (class 2606 OID 17028)
-- Name: services services_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.services
    ADD CONSTRAINT services_pkey PRIMARY KEY (serviceid);


--
-- TOC entry 4834 (class 2606 OID 17111)
-- Name: serviceusage serviceusage_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.serviceusage
    ADD CONSTRAINT serviceusage_pkey PRIMARY KEY (serviceusageid);


--
-- TOC entry 4832 (class 2606 OID 17093)
-- Name: stayoccupants stayoccupants_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stayoccupants
    ADD CONSTRAINT stayoccupants_pkey PRIMARY KEY (stayid, guestid);


--
-- TOC entry 4830 (class 2606 OID 17077)
-- Name: stays stays_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stays
    ADD CONSTRAINT stays_pkey PRIMARY KEY (stayid);


--
-- TOC entry 4840 (class 2606 OID 17059)
-- Name: bookingoccupants bookingoccupants_bookingid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bookingoccupants
    ADD CONSTRAINT bookingoccupants_bookingid_fkey FOREIGN KEY (bookingid) REFERENCES public.bookings(bookingid);


--
-- TOC entry 4841 (class 2606 OID 17064)
-- Name: bookingoccupants bookingoccupants_guestid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bookingoccupants
    ADD CONSTRAINT bookingoccupants_guestid_fkey FOREIGN KEY (guestid) REFERENCES public.guests(guestid);


--
-- TOC entry 4838 (class 2606 OID 17046)
-- Name: bookings bookings_categoryid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bookings
    ADD CONSTRAINT bookings_categoryid_fkey FOREIGN KEY (categoryid) REFERENCES public.roomcategories(categoryid);


--
-- TOC entry 4839 (class 2606 OID 17041)
-- Name: bookings bookings_clientid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bookings
    ADD CONSTRAINT bookings_clientid_fkey FOREIGN KEY (clientid) REFERENCES public.guests(guestid);


--
-- TOC entry 4836 (class 2606 OID 17010)
-- Name: roomcategoryfeatures roomcategoryfeatures_categoryid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roomcategoryfeatures
    ADD CONSTRAINT roomcategoryfeatures_categoryid_fkey FOREIGN KEY (categoryid) REFERENCES public.roomcategories(categoryid);


--
-- TOC entry 4837 (class 2606 OID 17015)
-- Name: roomcategoryfeatures roomcategoryfeatures_featureid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roomcategoryfeatures
    ADD CONSTRAINT roomcategoryfeatures_featureid_fkey FOREIGN KEY (featureid) REFERENCES public.features(featureid);


--
-- TOC entry 4835 (class 2606 OID 16989)
-- Name: rooms rooms_categoryid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms
    ADD CONSTRAINT rooms_categoryid_fkey FOREIGN KEY (categoryid) REFERENCES public.roomcategories(categoryid);


--
-- TOC entry 4846 (class 2606 OID 17117)
-- Name: serviceusage serviceusage_serviceid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.serviceusage
    ADD CONSTRAINT serviceusage_serviceid_fkey FOREIGN KEY (serviceid) REFERENCES public.services(serviceid);


--
-- TOC entry 4847 (class 2606 OID 17112)
-- Name: serviceusage serviceusage_stayid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.serviceusage
    ADD CONSTRAINT serviceusage_stayid_fkey FOREIGN KEY (stayid) REFERENCES public.stays(stayid);


--
-- TOC entry 4844 (class 2606 OID 17099)
-- Name: stayoccupants stayoccupants_guestid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stayoccupants
    ADD CONSTRAINT stayoccupants_guestid_fkey FOREIGN KEY (guestid) REFERENCES public.guests(guestid);


--
-- TOC entry 4845 (class 2606 OID 17094)
-- Name: stayoccupants stayoccupants_stayid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stayoccupants
    ADD CONSTRAINT stayoccupants_stayid_fkey FOREIGN KEY (stayid) REFERENCES public.stays(stayid);


--
-- TOC entry 4842 (class 2606 OID 17083)
-- Name: stays stays_bookingid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stays
    ADD CONSTRAINT stays_bookingid_fkey FOREIGN KEY (bookingid) REFERENCES public.bookings(bookingid);


--
-- TOC entry 4843 (class 2606 OID 17078)
-- Name: stays stays_roomid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stays
    ADD CONSTRAINT stays_roomid_fkey FOREIGN KEY (roomid) REFERENCES public.rooms(roomid);


-- Completed on 2025-05-01 16:38:28

--
-- PostgreSQL database dump complete
--

