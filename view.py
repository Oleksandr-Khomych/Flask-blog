from app import app
from flask import render_template, request, redirect, url_for, flash, session, g
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash   # Це фласкові функції для роботи з паролями і хешем
import sqlite3
from DataBase import DataBase
from UserLogin import UserLogin
import datetime


tmp_hash = 'pbkdf2:sha256:150000$PSRxViBL$4f84a1422b08ec8b3a75524f61f8ad0528b469d182e23dec09eabdfcc72ef92e'  #123qwe

login_manager = LoginManager(app)
dbase = None


@login_manager.user_loader
def load_user(user_id):
    db = get_db()
    dbase = DataBase(db)
    return UserLogin().fromDB(user_id, dbase)


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def Home():
    db = get_db()
    dbase = DataBase(db)
    user = dbase.getUser(current_user.get_id())
    return render_template('home.html', user=user)


@app.route('/auth', methods=('GET', 'POST'))
def auth():
    db = get_db()
    dbase = DataBase(db)
    if request.method == 'POST':
        user = dbase.getUserByLogin(request.form['login'])
        if user and check_password_hash(user['password_hash'], request.form['password']):
            userLogin = UserLogin().create(user)
            login_user(userLogin)
            return redirect(url_for('blog'))
        else:
            flash('Invalid login / password')
    else:
        if current_user.get_id():
            user_login = dbase.getUser(current_user.get_id())['login']
            return redirect(url_for('profile_next', login=user_login))
        return render_template('auth.html')


@app.route('/blog')
def blog():
    db = get_db()
    dbase = DataBase(db)
    user = dbase.getUser(current_user.get_id())
    # ===
    all_posts = dbase.getAllPosts()
    query = request.args.get('query')
    relevant_posts = []
    if query:
        query = query.lower()
        for i in all_posts:
            if query in i['title'].lower():
                relevant_posts.append(i)
            elif query in i['body'].lower():
                relevant_posts.append(i)
    else:
        relevant_posts = all_posts
    # ---
    return render_template('blog.html', user=user, posts=relevant_posts)


def get_db():
    '''З'єднання з БД, якщо воно ще не встановлено'''
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.route('/registration', methods=('GET', 'POST'))
def registration():
    if request.method == 'POST':
        db = get_db()
        dbase = DataBase(db)
        if request.form['password'] == request.form['password_repeat']:
            if len(request.form['username']) > 3 and len(request.form['login']) > 3:
                if not dbase.check_username(request.form['username']):
                    if not dbase.check_login(request.form['login']):
                        today = datetime.date.today()
                        password_hash = generate_password_hash(request.form['password'])
                        dbase.addUser(username=request.form['username'], login=request.form['login'], password_hash=password_hash, registration_date=today)
                        flash('User successfully registered')
                        return redirect(url_for('auth'))
                    else:
                        flash('Error. login exist in database!')
                else:
                    flash('Error. username exist in database!')
            else:
                flash('Error. Username or login is too short. Need 3+ sumvol')

        else:
            flash('Error. Passwords repeat are not the same')
    return render_template('registration.html')


@app.teardown_appcontext
def close_db(error):
    '''Закриваємо з'єдання з базою данних, якщо воно було встановлено'''
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route('/profile/<login>')
def profile_next(login):
    db = get_db()
    dbase = DataBase(db)
    user = dbase.getUser(current_user.get_id())
    if user:
        username = f"Username : {user['username']}"
        login = f'Login : {user["login"]}'
        date_register = f"Registration Date: {user['registration_date']}"
        post_count = f'Number of publications : {len(dbase.getPostsbyAuthorId(user["id"]))}'
        return render_template('profile.html', user=user, username=username, login=login, date_register=date_register,
                               post_count=post_count)
    return render_template('profile.html')


@app.route('/logout')
def logout():
    logout_user()
    flash('You are logged out')
    return redirect(url_for('auth'))


@app.route('/create_post', methods=('GET', 'POST'))
def create_post():
    db = get_db()
    dbase = DataBase(db)
    user = dbase.getUser(current_user.get_id())
    if request.method == 'POST':
        user = dbase.getUser(current_user.get_id())
        dbase.addPost(user['id'], request.form['title'], request.form['body'])
        flash('New post created!')
    return render_template('create_post.html', user=user)


@app.route('/blog/<post_id>')
def post(post_id):
    db = get_db()
    dbase = DataBase(db)
    post_id = post_id[4:]
    post = dbase.getPost(post_id)
    author = dbase.getUser(post['author_id'])
    author = author['username']
    user = dbase.getUser(current_user.get_id())
    return render_template('post.html', user=user, post=post, author=author)
