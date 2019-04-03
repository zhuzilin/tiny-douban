DROP TABLE IF EXISTS genre CASCADE;
CREATE TABLE genre (
    genre_id int,
    genre_name text,
    PRIMARY KEY (genre_id)
);
COPY genre FROM '/home/zhuzilin/Documents/w4111/project1/origin_data/genres.csv' DELIMITERS ',' CSV HEADER;
SELECT COUNT(*)
FROM genre;