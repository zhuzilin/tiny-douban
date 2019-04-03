-- According to our discussion with TA, 
-- to eliminate redundancy,
-- it is better not to meet the at least one constraint
-- in the schema, but in the application layer.

CREATE TABLE movie (
    movie_id int,
    adult boolean,
    lang text,
    title text NOT NULL,
    overview text,
    popularity float,
    homepage text,
	poster_path text,
    runtime int,
    budget int,
    revenue int,
	release_date date,
    PRIMARY KEY (movie_id)
)

CREATE TABLE customer (
    customer_id int,
    username text NOT NULL,
    password text NOT NULL,
    PRIMARY KEY (customer_id)
)

CREATE TABLE customer_comment_movie (
    customer_id int,
    movie_id int,
    rate int NOT NULL,
    content text,
    PRIMARY KEY (customer_id. movie_id),
    FOREIGN KEY (customer_id) REFERENCES customer,
    FOREIGN KEY (movie_id) REFERENCES movie
)

CREATE TABLE staff(
    staff_id int PRIMARY KEY,
	gender int,
    name text NOT NULL,
    profile_path text
)

CREATE TABLE movie_cast ( -- actor table
    movie_id int,
    staff_id int,
    role text NOT NULL,
	ordr int,
    PRIMARY KEY (movie_id, staff_id, role),
    FOREIGN KEY movie_id REFERENCES movie,
    FOREIGN KEY staff_id REFERENCES staff
)

CREATE TABLE movie_crew ( -- crew table
    movie_id int,
    staff_id int,
    job text NOT NULL,
    department text NOT NULL,
    PRIMARY KEY (movie_id, staff_id, job, department),
    FOREIGN KEY movie_id REFERENCES movie,
    FOREIGN KEY staff_id REFERENCES staff
)

CREATE TABLE production_company (
    company_id int,
    company_name text,
    PRIMARY KEY (company_id)
)

CREATE TABLE company_release_movie (
    movie_id int,
    company_id int,
    PRIMARY KEY (movie_id, staff_id),
    FOREIGN KEY movie_id REFERENCES movie,
    FOREIGN KEY company_id REFERENCES production_company
)

CREATE TABLE production_country (
    country_id int,
    country_name text,
    PRIMARY KEY (country_id)
)

CREATE TABLE country_release_movie (
    movie_id int,
    country_id int,
    PRIMARY KEY (movie_id, country_id),
    FOREIGN KEY movie_id REFERENCES movie,
    FOREIGN KEY country_id REFERENCES production_country
)

CREATE TABLE genre (
    genre_id int,
    genre_name text,
    PRIMARY KEY (genre_id)
)

CREATE TABLE movie_belong_genre (
    movie_id int,
    genre_id int,
    PRIMARY KEY (movie_id, genre_id),
    FOREIGN KEY movie_id REFERENCES movie,
    FOREIGN KEY genre_id REFERENCES genre
)

CREATE TABLE keyword (
    kw_id int,
    kw_name text,
    PRIMARY KEY (kw_id)
)

CREATE TABLE movie_has_kw (
    movie_id int,
    kw_id int,
    PRIMARY KEY (movie_id, kw_id),
    FOREIGN KEY movie_id REFERENCES movie,
    FOREIGN KEY kw_id REFERENCES keyword
)