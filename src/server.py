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
    print(request.args)
    login = False
    if 'username' in session:
        print('your are logged in with {}'.format(session['username']))
        login = True
    cursor = g.conn.execute("""
with rk(movie_id,rating) as ( 
    select r.movie_id, avg(r.rate)
    from customer_comment_movie r
    group by r.movie_id
    having count(*) > 1000
    order by avg(r.rate) desc
    limit 5)
select m.title, m.movie_id, m.poster_path, r.rating
from movie m, rk r
where m.movie_id = r.movie_id;
""")
    all_time_best = cursor.fetchall()

    return render_template('index.html', all_time_bests=all_time_best)


@app.route('/movie/<int:movie_id>')
def movie(movie_id):
    cursor = g.conn.execute("""
SELECT *
FROM movie
WHERE movie_id = {}
    """.format(movie_id))
    movie = cursor.first()
    print(movie['movie_id'])
    cursor = g.conn.execute("""
SELECT rate, COUNT(*)
FROM customer_comment_movie
WHERE movie_id = {}
GROUP BY rate
    """.format(movie_id))
    ratings = []
    for result in cursor:
        ratings.append(result)    # can also be accessed using result[0]
    cursor.close()
    return render_template("movie.html", movie=movie, ratings=ratings)


# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
    pass


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        cursor = g.conn.execute("""
SELECT customer_id AS uid
FROM customer
WHERE username = {} AND password = {}
        `   `""".format(request.form['username'], request.form['pw']))
        uid =
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
          <form method="post">
              <p><input type=text name=username>
              <p><input type=submit value=Login>
          </form>
    '''


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
