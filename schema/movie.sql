-- According to our discussion with TA, 
-- to eliminate redundancy,
-- it is better not to meet the at least one constraint
-- in the schema, but in the application layer.

DROP TABLE IF EXISTS movie CASCADE;
CREATE TABLE movie (
    movie_id int,
    adult boolean,
    lang text,
    title text NOT NULL,
    overview text,
    homepage text,
	poster_path text,
    runtimes float,
    budget float,
    revenue float,
	release_date date,
    PRIMARY KEY (movie_id)
);
COPY movie FROM '/home/zhuzilin/Documents/w4111/project1/origin_data/movies.csv' DELIMITERS ',' CSV HEADER;
SELECT COUNT(*)
FROM movie;


