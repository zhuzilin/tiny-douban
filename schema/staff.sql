DROP TABLE IF EXISTS staff CASCADE;
CREATE TABLE staff(
    staff_id int PRIMARY KEY,
	gender int,
    name text NOT NULL,
    profile_path text
);
COPY staff FROM '/home/zhuzilin/Documents/w4111/project1/origin_data/staff.csv' DELIMITERS ',' CSV HEADER;
SELECT COUNT(*)
FROM staff;