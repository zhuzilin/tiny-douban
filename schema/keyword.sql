DROP TABLE IF EXISTS keyword CASCADE;
CREATE TABLE keyword (
    kw_id int,
    kw_name text,
    PRIMARY KEY (kw_id)
);
COPY keyword FROM '/home/zhuzilin/Documents/w4111/project1/origin_data/keywords.csv' DELIMITERS ',' CSV HEADER;
SELECT COUNT(*)
FROM keyword;