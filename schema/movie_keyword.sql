DROP TABLE IF EXISTS movie_has_kw CASCADE;
CREATE TABLE movie_has_kw (
    movie_id int,
    kw_id int,
    PRIMARY KEY (movie_id, kw_id),
    FOREIGN KEY (movie_id) REFERENCES movie(movie_id),
    FOREIGN KEY (kw_id) REFERENCES keyword(kw_id)
);
COPY movie_has_kw FROM '/home/zhuzilin/Documents/w4111/project1/origin_data/movie_keywords.csv' DELIMITERS ',' CSV HEADER;
SELECT COUNT(*)
FROM movie_has_kw;