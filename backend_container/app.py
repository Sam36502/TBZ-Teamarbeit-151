from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from passlib.context import CryptContext
import json
import MySQLdb.cursors
import re

app = Flask(__name__)

app.secret_key = 'somesecretkey'

app.config['MYSQL_HOST'] = '172.17.0.4'
app.config['MYSQL_USER'] = 'ann_mem_user'
app.config['MYSQL_PASSWORD'] = '4nn_m3m'
app.config['MYSQL_DB'] = 'annales_memum'

db = MySQL(app)


pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=30000
)


def encrypt_password(password):
    return pwd_context.encrypt(password)


def check_encrypted_password(password, hashed):
    return pwd_context.verify(password, hashed)


@app.route('/')
def home():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        'SELECT id_page, creator_user_id, title, text, is_deleted FROM tbl_page')
    entries = cursor.fetchall()

    return render_template('index.html', username=session['username'], entries=entries)


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM tbl_user WHERE username = %s', [username])
        account = cursor.fetchone()
        if account:
            if check_encrypted_password(password, account['password']):
                session['loggedin'] = True
                session['id'] = account['id_user']
                session['username'] = account['username']
                msg = 'Logged in successfully !'
                return redirect('/')
        msg = 'Incorrect username / password !'
    return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM tbl_user WHERE username = %s', [username])
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers'
        elif not username or not password:
            msg = 'Please fill out the form'
        else:
            cursor.execute(
                'INSERT INTO tbl_user(username, password) VALUES (%s, %s)', [username, encrypt_password(password)])
            db.connection.commit()
            msg = 'You have successfully registered'
    elif request.method == 'POST':
        msg = 'Please fill out the form'
    return render_template('register.html', msg=msg)


@app.route('/newEntry', methods=['GET', 'POST'])
def newEntry():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    msg = ''

    if (request.method == 'POST' and 'title' in request.form and 'description' in request.form):
        title = request.form['title']
        description = request.form['description']

        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM tbl_page WHERE title = %s', [title])
        page = cursor.fetchone()
        if page:
            msg = 'This Page already exists!'
        elif not title or not description:
            msg = 'Please fill out the form'
        else:
            cursor.execute(
                'INSERT INTO tbl_page(creator_user_id, title, text) VALUES (%s, %s, %s)', [session['id'], title, description])
            db.connection.commit()
            return redirect('/')
    elif request.method == 'POST':
        msg = "Please fill out the form"

    return render_template('newEntry.html', msg=msg)


@app.route('/editEntry/<pageId>', methods=['GET', 'POST'])
def editEntry(pageId):
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    msg = ''

    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        'SELECT id_page, creator_user_id, title, text, is_deleted FROM tbl_page where id_page = %s', [pageId])
    entry = cursor.fetchone()

    if entry:
        if session['id'] != entry['creator_user_id']:
            return redirect('/')

        if (request.method == 'POST' and 'title' in request.form and 'description' in request.form):
            title = request.form['title']
            description = request.form['description']

            if not title or not description:
                msg = 'Please fill out the form'
            else:
                cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute(
                'UPDATE tbl_page SET title=%s, text=%s WHERE id_page = %s', [title, description, pageId])
                db.connection.commit()
                
                return redirect('/')

        return render_template('/updateEntry.html', entry=entry, msg=msg)
    return redirect('/')

@app.route('/deleteEntry/<pageId>')
def deleteEntry(pageId):
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        'SELECT id_page, creator_user_id, title, text, is_deleted FROM tbl_page where id_page = %s', [pageId])
    entry = cursor.fetchone()

    if entry:
        if session['id'] != entry['creator_user_id']:
            return redirect('/')

        cursor.execute(
            'UPDATE tbl_page SET is_deleted=1 WHERE id_page = %s', [pageId])
        db.connection.commit()
        return redirect('/')

app.run(host='0.0.0.0')
