DROP TABLE IF EXISTS movie_crew CASCADE;
CREATE TABLE movie_crew ( -- crew table
    movie_id int,
    staff_id int,
    job text NOT NULL,
    department text NOT NULL,
    PRIMARY KEY (movie_id, staff_id, job, department),
    FOREIGN KEY (movie_id) REFERENCES movie(movie_id),
    FOREIGN KEY (staff_id) REFERENCES staff(staff_id)
);
COPY movie_crew FROM '/home/zhuzilin/Documents/w4111/project1/origin_data/movieid_crew.csv' DELIMITERS ',' CSV HEADER;
SELECT COUNT(*)
FROM movie_crew;