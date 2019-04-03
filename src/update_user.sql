CREATE TEMP TABLE c (
    customer_id int,
    username text NOT NULL,
    password text NOT NULL,
    PRIMARY KEY (customer_id)
);
COPY c FROM '/home/zhuzilin/Documents/w4111/project1/origin_data/user_new.csv' DELIMITERS ',' CSV HEADER;

UPDATE customer
SET username = c.username
FROM c
WHERE c.customer_id = customer.customer_id;

DROP TABLE c;