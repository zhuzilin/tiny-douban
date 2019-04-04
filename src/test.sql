with srk(movie_id, title, poster_path) as (
select m.movie_id, m.title, m.poster_path
from movie m, movie_cast ca
where (ca.staff_id = 192 and ca.movie_id = m.movie_id) 
union
select m.movie_id, m.title, m.poster_path
from movie m, movie_crew cr
where (cr.staff_id = 192 and cr.movie_id = m.movie_id)
)

select s.title, s.movie_id, s.poster_path, mr.rating
from movie_rating mr, srk s
where s.movie_id = mr.movie_id
order by mr.rating desc
limit 7;
