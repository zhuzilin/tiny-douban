DROP TABLE IF EXISTS movie_cast CASCADE;
CREATE TABLE movie_cast ( -- actor table
    movie_id int,
    staff_id int,
    role text NOT NULL,
	ordr int,
    PRIMARY KEY (movie_id, staff_id, role, ordr),
    FOREIGN KEY (movie_id) REFERENCES movie(movie_id),
    FOREIGN KEY (staff_id) REFERENCES staff(staff_id)
);
COPY movie_cast FROM '/home/zhuzilin/Documents/w4111/project1/origin_data/movie_cast.csv' DELIMITERS ',' CSV HEADER;
SELECT COUNT(*)
FROM movie_cast;