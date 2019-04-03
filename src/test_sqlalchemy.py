from sqlalchemy import create_engine
from env import get_env

env = get_env('local')
DB_USER = env['DB_USER']
DB_PASSWORD = env['DB_PW']
DB_SERVER = env['DB_IP']
DB_NAME = env['DB_NAME']

DATABASEURI = "postgresql://{}:{}@{}/{}".format(DB_USER, DB_PASSWORD, DB_SERVER, DB_NAME)

db = create_engine(DATABASEURI)

con = db.connect()

foo = con.execute("""
with rk(movie_id,rating) as
(select r.movie_id, avg(r.rate)
                from customer_comment_movie r
                group by r.movie_id
                having count(*) > 1000
                order by avg(r.rate) desc
                limit 10)
select m.title, r.rating
from movie m, rk r
where m.movie_id = r.movie_id;
""")

for record in foo:
    print(record)