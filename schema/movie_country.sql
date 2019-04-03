DROP TABLE IF EXISTS country_release_movie CASCADE;
CREATE TABLE country_release_movie (
    movie_id int,
    country_id text,
    PRIMARY KEY (movie_id, country_id),
    FOREIGN KEY (movie_id) REFERENCES movie(movie_id),
    FOREIGN KEY (country_id) REFERENCES production_country(country_id)
);
COPY country_release_movie FROM '/home/zhuzilin/Documents/w4111/project1/origin_data/country_movie.csv' DELIMITERS ',' CSV HEADER;
SELECT COUNT(*)
FROM country_release_movie;