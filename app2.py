# directory: cd "C:\Users\mabra\OneDrive\Desktop\463 Final Project"
# run sql: sqlite3 users.db
# show the table: SELECT * FROM users;
#logins:
"""
1|mabraham24|Andrew09
2|anil1234|Andrew#09
3|vini1234|Andrew#2009
4|andrew54|Andrew22
5|treasure21|Purplepancakes
6|batman2|Superman
7|ron123|Andrew
8|rini98|Ron01
9|eagles17|superbowl
"""

from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import random
import secrets


app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

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

# Hardcoded good news articles
good_news_articles = [
    {'title': 'Community Comes Together to Plant Trees', 'content': '...', 'source': 'Nature News', 'url': 'https://friendsoftrees.org/blog/why-we-come-together-to-plant-trees/'},
    {'title': 'Local Hero Rescues Stray Animals', 'content': '...', 'source': 'Animal Rescue Times', 'url': 'https://www.nbcnewyork.com/news/national-international/homeless-man-hailed-as-hero-for-running-into-burning-animal-shelter-to-save-animals/2803894/'},
    {'title': 'Students Achieve Record-Breaking Exam Results', 'content': '...', 'source': 'Education Weekly', 'url': 'https://ncbradford.ac.uk/2022/08/18/new-college-students-achieve-record-breaking-results-in-first-post-covid-year-%EF%BF%BC/'},
    # Add more articles as needed
]
def get_random_good_news():
    # Randomly select an article
    random_article = random.choice(good_news_articles)
    return [random_article]


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

    if user:
        if user[2] == password:  # Check if the password matches
            return render_template('menu.html', username=username)
        else:
            flash('Password not correct', 'error')
    else:
        flash('Username does not exist; Create a new account.', 'error')

    return redirect(url_for('home'))  # Redirect to home or login page
    
@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/stressometer')
def stressometer():
    return render_template('stressometer.html')

@app.route('/journaling')
def journaling():
    return render_template('journaling.html')


@app.route('/good-news')
def good_news():
    # Fetch a random good news article
    random_article = get_random_good_news()

    return render_template('good_news.html', articles=random_article)

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    conn.commit()

    conn.close()

    flash(f'Account created for {username}', 'success')
    return redirect(url_for('register'))  # Redirect to the register page after account creation



if __name__ == '__main__':
    app.run(debug=True)


