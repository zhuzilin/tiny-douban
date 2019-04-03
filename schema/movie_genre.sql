DROP TABLE IF EXISTS movie_belong_genre CASCADE;
CREATE TABLE movie_belong_genre (
    movie_id int,
    genre_id int,
    PRIMARY KEY (movie_id, genre_id),
    FOREIGN KEY (movie_id) REFERENCES movie(movie_id),
    FOREIGN KEY (genre_id) REFERENCES genre(genre_id)
);
COPY movie_belong_genre FROM '/home/zhuzilin/Documents/w4111/project1/origin_data/genres_movie.csv' DELIMITERS ',' CSV HEADER;
SELECT COUNT(*)
FROM movie_belong_genre;