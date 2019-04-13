import os
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, jsonify, session, url_for
from env import get_env

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
app.secret_key = b'zz2579&fl2504'

env = get_env('local')
DB_USER = env['DB_USER']
DB_PASSWORD = env['DB_PW']
DB_IP = env['DB_IP']
DB_NAME = env['DB_NAME']

DB_URI = "postgresql://{}:{}@{}/{}".format(DB_USER, DB_PASSWORD, DB_IP, DB_NAME)

# start the db engine
engine = create_engine(DB_URI)

@app.before_request
def before_request():
    """
    This function is run at the beginning of every web request
    (every time you enter an address in the web browser).
    We use it to setup a database connection that can be used throughout the request
    The variable g is globally accessible
    """
    try:
        g.conn = engine.connect()
    except:
        print("uh oh, problem connecting to database")
        import traceback
        traceback.print_exc()
        g.conn = None


@app.teardown_request
def teardown_request(exception):
    """
    At the end of the web request, this makes sure to close the database connection.
    If you don't the database could run out of memory!
    """
    try:
        g.conn.close()
    except Exception as e:
        pass

@app.route('/')
def index():
    # DEBUG: this is debugging code to see what request looks like
    if 'login' not in session:
        session['login'] = False
    if session['login']:
        print('your are logged in with {}'.format(session['username']))
    cursor = g.conn.execute("""
select m.title, m.movie_id, m.poster_path, r.rating
from movie m, movie_rating r
where m.movie_id = r.movie_id and r.count > 1000
limit 7
""")
    # cursor 的类型是resultproxy
    all_time_best = cursor.fetchall()

    # top 3 genre, top 7 movies
    cursor = g.conn.execute("""
with genre_rank as (
select genre_id
from movie_belong_genre
group by genre_id
order by count(*) desc
limit 4 )
select g.*
from genre g, genre_rank r
where g.genre_id = r.genre_id;
    """)
    most_genres = cursor.fetchall()
    best_genre_movies = {}
    for genre in most_genres:
        cursor = g.conn.execute("""
with movie_genre_rating as (
    select r.movie_id, r.rating
    from movie_belong_genre mg, movie_rating r
    where mg.genre_id = '{}' and mg.movie_id = r.movie_id and r.count > 1000
    order by r.rating desc
    limit 7
)
select m.title, m.movie_id, m.poster_path, r.rating
from movie_genre_rating r, movie m
where r.movie_id = m.movie_id;
            """.format(genre['genre_id']))
        best_genre_movies[genre['genre_name']] = (genre['genre_id'], cursor.fetchall())

    return render_template('index.html',
                           all_time_bests=all_time_best,
                           best_genre_movies=best_genre_movies,
                           login=session['login'])


@app.route('/movie/<int:movie_id>')
def movie(movie_id):
    if 'login' not in session:
        session['login'] = False
    # basic movie info
    cursor = g.conn.execute("""
SELECT *
FROM movie
WHERE movie_id = {}
    """.format(movie_id))
    movie = cursor.first()

    # rating distribution
    cursor = g.conn.execute("""
SELECT rate, COUNT(*)
FROM customer_comment_movie
WHERE movie_id = {}
GROUP BY rate
    """.format(movie_id))
    ratings = [0] * 10
    for row in cursor:
        ratings[int(10 - row[0] * 2)] = row[1]
    cursor.close()

    # staff info
    # director
    cursor = g.conn.execute("""
SELECT s.*
FROM movie_crew mc, staff s
WHERE mc.movie_id = {} AND mc.staff_id = s.staff_id AND mc.job='Director'
        """.format(movie_id))
    # main actor
    staffs = cursor.fetchall()
    # assert len(staffs) == 1
    cursor = g.conn.execute("""
SELECT s.*
FROM movie_cast mc, staff s
WHERE mc.movie_id = {} AND mc.staff_id = s.staff_id
ORDER BY mc.ordr
LIMIT 6
    """.format(movie_id))
    staffs += cursor.fetchall()

    # genre
    cursor = g.conn.execute("""
    SELECT g.*
    FROM movie_belong_genre mg, genre g
    WHERE mg.movie_id = {} AND mg.genre_id = g.genre_id
        """.format(movie_id))
    genre = cursor.fetchall()

    # company
    cursor = g.conn.execute("""
            SELECT c.company_name AS name
            FROM company_release_movie mc, production_company c
            WHERE mc.movie_id = {} AND mc.company_id = c.company_id
                """.format(movie_id))
    companies = cursor.fetchall()

    # country
    cursor = g.conn.execute("""
        SELECT c.country_name AS name
        FROM country_release_movie mc, production_country c
        WHERE mc.movie_id = {} AND mc.country_id = c.country_id
            """.format(movie_id))
    countries = cursor.fetchall()
    return render_template("movie.html",
                           movie=movie,
                           ratings=ratings,
                           staffs=staffs,
                           genres=genre,
                           companies=companies,
                           countries=countries,
                           login=session['login'])


@app.route('/user/<int:user_id>')
def user(user_id):
    if 'login' not in session:
        session['login'] = False
    else:
        user_id = session['uid']
    cursor = g.conn.execute("""
select 
    """)

@app.route('/staff/<int:staff_id>')
def staff(staff_id):
    if 'login' not in session:
        session['login'] = False
    cursor = g.conn.execute("""
SELECT * 
FROM staff
WHERE staff_id = {}
    """.format(staff_id))
    staff = cursor.first()

    cursor = g.conn.execute("""
with srk(movie_id, title, poster_path) as (
select m.movie_id, m.title, m.poster_path
from movie m, movie_cast ca
where (ca.staff_id = {} and ca.movie_id = m.movie_id)
union
select m.movie_id, m.title, m.poster_path
from movie m, movie_crew cr
where (cr.staff_id = {} and cr.movie_id = m.movie_id)
)

select s.title, s.movie_id, s.poster_path, mr.rating
from movie_rating mr, srk s
where s.movie_id = mr.movie_id
order by mr.rating DESC
limit 7
    """.format(staff_id,staff_id))
    staff_best_movie = cursor.fetchall()
    cursor = g.conn.execute("""
with cs(staff_id, name, profile_path) as (
select s.staff_id, s.name, s.profile_path
from movie_cast ca1, movie_cast ca2, staff s
where (ca1.staff_id = {} and ca1.movie_id = ca2.movie_id and ca2.staff_id = s.staff_id and s.profile_path is not NULL)
UNION
select s.staff_id, s.name, s.profile_path
from movie_crew cr1, movie_crew cr2, staff s
where (cr1.staff_id = {} and cr1.movie_id = cr2.movie_id and cr2.movie_id = s.staff_id and s.profile_path is not NULL)
)

select * from cs limit 7
    """.format(staff_id,staff_id))
    co_staff = cursor.fetchall()
    return render_template("staff.html", staff=staff, staff_best_movie=staff_best_movie, co_staff = co_staff, login=session['login'])


@app.route('/genre/<int:genre_id>')
def genre(genre_id):
    if 'login' not in session:
        session['login'] = False
    p = request.args.get('p')
    if p is None:
        p = 1
    else:
        p = int(p)

    cursor = g.conn.execute("""
with genre_movie as (
    select m.*
    from movie m, movie_belong_genre mg
    where mg.genre_id = {} and m.movie_id = mg.movie_id
)
select m.title, m.movie_id, m.poster_path, r.rating
from movie_rating r, genre_movie m
where r.movie_id = m.movie_id and r.count > 500
order by r.rating desc
limit 27 offset {};
        """.format(genre_id, 27*(p-1)))
    genre_movie = cursor.fetchall()

    cursor = g.conn.execute("""
select *
from genre
where genre_id = {};
                """.format(genre_id))
    genre = cursor.first()

    return render_template('genre.html',
                           genre=genre,
                           p=p,
                           genre_movie=genre_movie,
                           login=session['login'])


@app.route('/search')
def search():
    if 'login' not in session:
        session['login'] = False
    # search text
    text = request.args.get('text').lower()
    # type
    type = request.args.get('type')
    assert type in ['movie', 'staff', 'company', 'country'], "wrong type for search!"
    # page
    p = request.args.get('p')
    if p is None:
        p = 1
    else:
        p = int(p)
    if type == 'movie':
        cursor = g.conn.execute("""
SELECT m.title, m.movie_id, m.poster_path, r.rating, s.name AS director
FROM movie m, movie_rating r, movie_crew mc, staff s
WHERE r.movie_id = m.movie_id AND LOWER(m.title) LIKE '%%{}%%'
    AND mc.movie_id = m.movie_id AND mc.staff_id = s.staff_id AND mc.job='Director'
ORDER BY r.count DESC
limit 20 offset {};
            """.format(text, 20 * (p - 1)))

    result = cursor.fetchall()
    print(result)
    return render_template('search.html',
                           type=type,
                           text=text,
                           result=result,
                           p=p,
                           login=session['login'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print(request.form)
        cursor = g.conn.execute("""
SELECT customer_id AS uid, username, password
FROM customer

WHERE username = '{}' AND password = '{}';
""".format(request.form['username'], request.form['password']))
        user = cursor.first()
        if user is None:
            print("fail to login")
        else:
            session['uid'] = user['uid']
            session['username'] = user['username']
            session['password'] = user['password']
            session['login'] = True
            print(session['uid'])
            return redirect(url_for('index'))

    return render_template("login.html", login=session['login'])


@app.route('/logout')
def logout():
    keys = list(session.keys())
    for key in keys:
        session.pop(key)
    session['login'] = False
    def redirect_url(default='index'):
        return request.args.get('next') or \
               request.referrer or \
               url_for(default)

    return redirect(redirect_url())


if __name__ == "__main__":
    import click

    @click.command()
    @click.option('--debug', is_flag=True)
    @click.option('--threaded', is_flag=True)
    @click.argument('HOST', default='0.0.0.0')
    @click.argument('PORT', default=5000, type=int)
    def run(debug, threaded, host, port):
        """
        This function handles command line parameters.
        Run the server using
                python server.py
        Show the help text using
                python server.py --help
        """

        HOST, PORT = host, port
        print("running on %s:%d" % (HOST, PORT))
        app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)
    run()
