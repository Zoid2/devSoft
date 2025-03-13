from flask import Flask, render_template, request, redirect, url_for, flash, g
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
DATABASE = 'stories.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def execute_db(query, args=()):
    db = get_db()
    db.execute(query, args)
    db.commit()

@app.route('/')
def index():
    stories = query_db('SELECT * FROM stories')
    return render_template('index.html', stories=stories)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')
        
        execute_db('INSERT INTO users (username, password) VALUES (?, ?)', [username, hashed_password])
        
        flash('You have successfully signed up!', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = query_db('SELECT * FROM users WHERE username = ?', [username], one=True)
        if user and check_password_hash(user[2], password):
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html')

@app.route('/create_story', methods=['GET', 'POST'])
def create_story():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        execute_db('INSERT INTO stories (title, content) VALUES (?, ?)', [title, content])
        
        return redirect(url_for('index'))
    return render_template('create_story.html')

@app.route('/contribute/<int:story_id>', methods=['GET', 'POST'])
def contribute(story_id):
    story = query_db('SELECT * FROM stories WHERE id = ?', [story_id], one=True)
    if request.method == 'POST':
        contribution = request.form['contribution']
        new_content = story[2] + f"\n\n{contribution}"
        execute_db('UPDATE stories SET content = ? WHERE id = ?', [new_content, story_id])
        return redirect(url_for('index'))
    return render_template('contribute.html', story=story)

if __name__ == '__main__':
    app.run(debug=True)
