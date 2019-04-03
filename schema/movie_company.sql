DROP TABLE IF EXISTS company_release_movie CASCADE;
CREATE TABLE company_release_movie (
    movie_id int,
    company_id int,
    PRIMARY KEY (movie_id, company_id),
    FOREIGN KEY (movie_id) REFERENCES movie(movie_id),
    FOREIGN KEY (company_id) REFERENCES production_company(company_id)
);
COPY company_release_movie FROM '/home/zhuzilin/Documents/w4111/project1/origin_data/company_movie.csv' DELIMITERS ',' CSV HEADER;
SELECT COUNT(*)
FROM company_release_movie;