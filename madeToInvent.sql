DROP DATABASE IF EXISTS made_to_invent_db;



 CREATE DATABASE made_to_invent_db;
 \c made_to_invent_db



CREATE TABLE users(

    username TEXT PRIMARY KEY,
    password  TEXT NOT NULL,
    firstname TEXT NOT NULL,
    middlename  TEXT ,
    lastname TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NULL
    -- CONSTRAINT fk_company
    -- FOREIGN KEY(company_id)
    -- REFERENCES company(company_id)
    -- ON DELETE SET NULL
    );

    CREATE TABLE company(

    id INTEGER PRIMARY KEY,
    name  TEXT NOT NULL,
    contact TEXT,
    email TEXT,
    phone TEXT


    );


      CREATE TABLE users(

    id INTEGER PRIMARY KEY,
    first_name  TEXT NOT NULL,
    last_name TEXT NOT NULL,
    image_url TEXT NOT NULL

    );


--  INSERT INTO inventors (username,user_password,first_name,middle_name ,last_name,email) values ('shylapathiyal','patents','Shyla',null,'Pathiyal','spathiyal@gmail.com')
--     phone_number TEXT NOT NULL
--    CONSTRAINT fk_compny
--       FOREIGN KEY(company_id)
-- 	  REFERENCES company(company_id)
-- 	  ON DELETE SET NULL


-- insert into users (username,password,firstname,middlename,lastname,email)values ('spathiyal','s','s','s','s','s');

insert into users (first_name,last_name,image_url)values ('shyla','pathiyal',NULL);



-- CREATE TABLE company(
--     company_id SERIAL PRIMARY KEY,
--     company_name TEXT NOT NULL,
--     contact_name TEXT NOT NULL,
--     contact_email TEXT NOT NULL,
--     contact_phone_number TEXT NOT NULL,
--     company_address   TEXT NOT NULL
-- )

-- CREATE TABLE patents(
--     patent_id SERIAL PRIMARY KEY,
--     patent_number TEXT NOT NULL(unique),
--     patent_name TEXT NOT NULL,
--     invented_date TEXT NOT NULL,
--     summary TEXT NOT NULL,
--     descr TEXT NOT NULL,
--     metric TEXT
--     -- need to check if this has to be sepeated into differnt tables
-- )

-- CREATE TABLE inventors_patents(
--     id SERIAL PRIMARY KEY,
--     patent_id TEXT NOT NULL,
--     inventor_id  TEXT NOT NULL

-- )