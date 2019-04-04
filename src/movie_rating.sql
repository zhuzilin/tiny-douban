DROP TABLE IF EXISTS movie_rating CASCADE;
CREATE TABLE movie_rating(movie_id,rating) as
    (select movie_id, avg(rate), count(*)
    from customer_comment_movie
    group by movie_id
    order by avg(rate) desc);