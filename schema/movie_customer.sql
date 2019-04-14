DROP TABLE IF EXISTS customer_comment_movie CASCADE;
CREATE TABLE customer_comment_movie (
    customer_id int,
    rate float NOT NULL,
    movie_id int,
    content text,
    PRIMARY KEY (customer_id, movie_id),
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
    FOREIGN KEY (movie_id) REFERENCES movie(movie_id)
);
COPY customer_comment_movie FROM '/home/zhuzilin/Documents/w4111/project1/origin_data/rating.csv' DELIMITERS ',' CSV HEADER;
SELECT COUNT(*)
FROM customer_comment_movie;