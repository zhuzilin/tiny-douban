select s.name, count(*) as movie_number
from staff s, movie_cast mc, movie m
where s.staff_id = mc.staff_id and mc.movie_id = m.movie_id
group by s.staff_id
order by count(*) desc
limit 10;
