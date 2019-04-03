select c.country_name, count(*) as movie_number
from production_country c, country_release_movie cm, movie m
where c.country_id = cm.country_id and cm.movie_id = m.movie_id
group by c.country_id
order by count(*) desc
limit 10;