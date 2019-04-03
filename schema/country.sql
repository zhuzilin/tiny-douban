DROP TABLE IF EXISTS production_country CASCADE;
CREATE TABLE production_country (
    country_id text,
    country_name text,
    PRIMARY KEY (country_id)
);
COPY production_country FROM '/home/zhuzilin/Documents/w4111/project1/origin_data/country.csv' DELIMITERS ',' CSV HEADER;
SELECT COUNT(*)
FROM production_country;