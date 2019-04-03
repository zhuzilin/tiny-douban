DROP TABLE IF EXISTS customer CASCADE;
CREATE TABLE customer (
    customer_id int,
    username text NOT NULL,
    password text NOT NULL,
    PRIMARY KEY (customer_id)
);
COPY customer FROM '/home/zhuzilin/Documents/w4111/project1/origin_data/user.csv' DELIMITERS ',' CSV HEADER;
SELECT COUNT(*)
FROM customer;