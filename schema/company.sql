DROP TABLE IF EXISTS production_company CASCADE;
CREATE TABLE production_company (
    company_id int,
    company_name text,
    PRIMARY KEY (company_id)
);
COPY production_company FROM '/home/zhuzilin/Documents/w4111/project1/origin_data/company.csv' DELIMITERS ',' CSV HEADER;
SELECT COUNT(*)
FROM production_company