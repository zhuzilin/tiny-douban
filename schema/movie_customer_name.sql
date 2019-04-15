DROP TABLE IF EXISTS movie_customer_name CASCADE;
CREATE TABLE movie_customer_name(movie_id,movie_name,poster_path,rate,customer_id) as
    (select c.movie_id, m.title, m.poster_path,c.rate, c.customer_id
    from customer_comment_movie c, movie m
    where c.movie_id=m.movie_id);

select count(*) from movie_customer_name;
