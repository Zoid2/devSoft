from flask import Flask, render_template, request, redirect, url_for, flash, session, g
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
        hashed_password = generate_password_hash(password)
        
        try:
            execute_db('INSERT INTO users (username, password) VALUES (?, ?)', [username, hashed_password])
            flash('You have successfully signed up!', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists', 'danger')
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = query_db('SELECT * FROM users WHERE username = ?', [username], one=True)
        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

@app.route('/create_story', methods=['GET', 'POST'])
def create_story():
    if 'user_id' not in session:
        flash('You need to be logged in to create a story.', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        execute_db('INSERT INTO stories (title, content) VALUES (?, ?)', [title, content])
        flash('Story created successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('create_story.html')

@app.route('/contribute/<int:story_id>', methods=['GET', 'POST'])
def contribute(story_id):
    if 'user_id' not in session:
        flash('You need to be logged in to contribute to a story.', 'danger')
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    story = query_db('SELECT * FROM stories WHERE id = ?', [story_id], one=True)
    contribution_check = query_db('SELECT * FROM contributions WHERE user_id = ? AND story_id = ?', [user_id, story_id], one=True)
    
    if contribution_check:
        flash('You have already contributed to this story.', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        contribution = request.form['contribution']
        new_content = story[2] + f"\n\n{contribution}"
        execute_db('UPDATE stories SET content = ? WHERE id = ?', [new_content, story_id])
        execute_db('INSERT INTO contributions (user_id, story_id) VALUES (?, ?)', [user_id, story_id])
        flash('Contribution added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('contribute.html', story=story)

if __name__ == '__main__':
    app.run(debug=True)
