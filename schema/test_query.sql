with rk(movie_id,rating) as
(select r.movie_id, avg(r.rate)
				from customer_comment_movie r, country_release_movie mc, production_country c
				where r.movie_id = mc.movie_id and mc.country_id = c.country_id and c.country_name = 'China'
				group by r.movie_id
				having count(*) > 1000
				order by avg(r.rate) desc
				limit 10)
select m.title, r.rating
from movie m, rk r
where m.movie_id = r.movie_id;