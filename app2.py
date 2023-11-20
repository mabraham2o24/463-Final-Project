# directory: cd "C:\Users\mabra\OneDrive\Desktop\463 Final Project"
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Create a SQLite database
conn = sqlite3.connect('users.db')
c = conn.cursor()
c.execute('''
          CREATE TABLE IF NOT EXISTS users (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              username TEXT NOT NULL,
              password TEXT NOT NULL
          )
          ''')
conn.commit()
conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    c.execute('SELECT * FROM users WHERE username=?', (username,))
    user = c.fetchone()

    conn.close()

    if user and check_password_hash(user[2], password):
        return render_template('menu.html', username=username)
    else:
        return 'Incorrect username or password'

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/stressometer')
def stressometer():
    return render_template('stressometer.html')

@app.route('/journaling')
def journaling():
    return render_template('journaling.html')

@app.route('/good_news')
def good_news():
    return render_template('good_news.html')

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']

    hashed_password = generate_password_hash(password)

    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
    conn.commit()

    conn.close()

    return f'Account created for {username}'

if __name__ == '__main__':
    app.run(debug=True)
