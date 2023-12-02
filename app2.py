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
#improting neccessary modules from Flask and other libraries
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session
from datetime import datetime
import random

#initialize flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # secret key

# Create a SQLite database to store user info
conn = sqlite3.connect('users.db')
c = conn.cursor()
c.execute('''
          CREATE TABLE IF NOT EXISTS users (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              username TEXT NOT NULL,
              password TEXT NOT NULL
          )
          ''')
# Create 'user_entries' table to store journal entries
c.execute('''
          CREATE TABLE IF NOT EXISTS user_entries (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              user_id INTEGER NOT NULL,
              journal_content TEXT,
              timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
              FOREIGN KEY(user_id) REFERENCES users(id)
          )
          ''')

conn.commit()
conn.close()

# Hardcoded good news articles for different categories
good_news_articles = {
    'animals': [
        {'title': 'How These 2-Legged Dogs Inspire Humans Learning to Live With Amputations', 'content': 'Click Read More to Access The Article or Click Generate for Another Article', 'source': 'Daily Paws', 'url': ' https://www.dailypaws.com/2-legged-dogs-instagram-cyrus-lucky-deuce-7715487/', 'author': 'Austin Cannon'},        
        {'title': 'Partially Paralyzed Dog Starts Walking and Wagging His Tail in His New Home', 'content': 'Click Read More to Access The Article or Click Generate for Another Article', 'source': 'Daily Paws', 'url': 'https://www.dailypaws.com/partially-paralyzed-dog-adopted-after-hit-by-car-7775413/', 'Author': 'Austin Cannon'},
        {'title': 'Joey the 2-Legged Pup Went From Unadopted to Starring in the 2023 Puppy Bowl', 'content': 'Click Read More to Access The Article or Click Generate for Another Article', 'source': 'Daily Paws', 'url': 'https://www.dailypaws.com/pet-news-entertainment/feel-good-stories/joey-2-legged-dog-2023-puppy-bowl/', 'Author': 'Paige Mountain'},
        {'title': 'Amazing Cats and True Cat Stories', 'content': 'Click Read More to Access The Article or Click Generate for Another Article', 'source': 'Pet Helpful', 'url': 'https://pethelpful.com/cats/Amazing-Cats-and-True-Cat-Stories/', 'Author': 'Stephanie Henkel'},
        {'title': 'It’s International Cat Day. Here are 10 Inspiring Feline Stories to Celebrate', 'content': 'Click Read More to Access The Article or Click Generate for Another Article', 'source': 'CBS News', 'url': 'https://www.cbsnews.com/news/international-cat-day-august-8-2023-here-inspiring-feline-stories-to-celebrate/', 'Author': 'Caitlin O Kane'},

        # Add more articles for the 'animals' category
    ],
    'nature': [
        {'title': 'Peatland, Plastic and Phasing-Out Coal: Here’s Why Wales is Our Green Country of the Month', 'content': 'Click Read More to Access The Article or Click Generate for Another Article', 'source': 'Euro News', 'url': 'https://www.euronews.com/green/2023/10/31/peatland-plastic-and-phasing-out-coal-heres-why-wales-is-our-green-country-of-the-month/', 'Author': 'Euronews Green'},
        {'title': 'Celebrating 100 Million Trees Planted Since 2014', 'content': 'Click Read More to Access The Article or Click Generate for Another Article', 'source': 'One Tree Planted', 'url': 'https://onetreeplanted.org/blogs/newsroom/celebrating-100-million-trees/', 'Author': 'Meaghan Weeden'},
        {'title': 'Meet The Women Working to Grow Local Food Systems on U.S. Island Territories', 'content': 'Click Read More to Access The Article or Click Generate for Another Article', 'source': 'The 19th', 'url': 'https://19thnews.org/2023/05/women-locally-grown-food-sovereignty-us-island-territories/', 'Author': 'Jessica Kutz'},
        {'title': 'Climate ‘Victory’: Swiss Citizens Vote in Favour of New Law To Reach Net ', 'content': 'Click Read More to Access The Article or Click Generate for Another Article', 'source': 'Euro News', 'url': 'https://www.euronews.com/green/2023/06/19/electricity-sinkhole-or-important-step-forward-swiss-citizens-to-vote-on-new-climate-law/', 'Author': 'Lottie Lamb'},
        {'title': 'The 7 Natural Wonders of the World ', 'content': 'Click Read More to Access The Article or Click Generate for Another Article', 'source': 'World Atlas', 'url': 'https://www.worldatlas.com/places/the-7-natural-wonders-of-the-world.html/', 'Author': 'No Author'},

        # Add more articles for the 'nature' category
    ],
    'inspiring': [
        {'title': 'Beautiful and Inspiring Short Stories About Life', 'content': 'Click Read More to Access The Article or Click Generate for Another Article', 'source': 'Live Life Happy', 'url': 'https://livelifehappy.com/live-life-happy-stories/', 'Author': 'No Author'},
        {'title': 'Couple Plants 2 Million Trees in 20 Years to Restore Forest and Even the Animals Have Returned', 'content': 'Click Read More to Access The Article or Click Generate for Another Article', 'source': 'Good News Network', 'url': 'https://www.goodnewsnetwork.org/couple-plants-2-million-trees-in-20-years-to-restore-a-destroyed-forest-and-even-the-animals-have-returned/ ', 'Author': 'Andy Corbley'},
        {'title': 'Secret Donor Gives and Gives for 25 Years to Fund Education and Help for Destitute Families in China', 'content': 'Click Read More to Access The Article or Click Generate for Another Article', 'source': 'Good News', 'url': 'https://www.goodnewsnetwork.org/secret-donor-gives-and-gives-for-25-years-to-fund-education-and-help-for-destitute-families-in-china/ ', 'Author': 'Andy Corbley'},
        {'title': 'Mom Channeled Her Terminal Cancer Into Debt Relief Fundraiser-WIping Out $65 Million in Medical Debt', 'content': 'Click Read More to Access The Article or Click Generate for Another Article', 'source': 'Good News Network', 'url': 'https://www.goodnewsnetwork.org/mother-and-wife-channeled-terminal-cancer-into-debt-relief-fundraiser-wiping-out-65-million-in-medical-debt/', 'Author': 'Andy Corbley'},
        {'title': 'Selfless Quad Amputee Summits a Peak to Raise Money for Other Disabled Kids', 'content': 'Click Read More to Access The Article or Click Generate for Another Article', 'source': 'Good News Network', 'url': 'https://www.goodnewsnetwork.org/selfless-quad-amputee-hopes-to-summit-peak-to-raise-money-for-other-disabled-kids/', 'Author': 'Andy Corbley'},

        # Add more articles for the 'inspiring' category
    ],
    'laughs': [
        {'title': 'What Someone Who Doesn’t Own a Dog Imagines Owning a Dog is Like', 'content': 'Click Read More to Access The Article or Click Generate for Another Article', 'source': 'The New Yorker', 'url': 'https://www.newyorker.com/humor/daily-shouts/what-someone-who-doesnt-own-a-dog-imagines-owning-a-dog-is-like/', 'Author': 'Chris Scott'},
        {'title': 'The Internet is Living for This Teen’s Brush with the Law in Full Shrek Makeup ', 'content': 'Click Read More to Access The Article or Click Generate for Another Article', 'source': 'Time', 'url': 'https://time.com/4994897/shrek-teen-cops/', 'Author': 'Raisa Bruner'},
        {'title': '50+ Short Funny Stories That Will Crack You Up in 60 Seconds', 'content': 'Click Read More to Access The Article or Click Generate for Another Article', 'source': 'Thought Catalog', 'url': 'https://thoughtcatalog.com/january-nelson/2018/06/funny-stories/', 'Author': 'January Nelson'},
        {'title': 'Horse Joins Cycle Race', 'content': 'Click Read More to Access The Article or Click Generate for Another Article', 'source': 'Keep Laughing Forever', 'url': 'https://www.keeplaughingforever.com/post/horse-joins-cycle-race/', 'Author': 'B-Man'},
        {'title': 'DC-Area Residents Share Funny and Strange Thanksgiving Memories', 'content': 'Click Read More to Access The Article or Click Generate for Another Article', 'source': 'Wtop News', 'url': 'https://wtop.com/thanksgiving-news/2023/11/dc-area-residents-share-some-funny-and-strange-thanksgiving-memories/', 'Author': 'Ivy Lyons'},

        # Add more articles for the 'laughs' category
    ],
    
}

def get_random_good_news(category):
    # Randomly select an article from the specified category
    return random.choice(good_news_articles.get(category, []))

def calculate_overall_mood(answers):
    # Calculate the overall mood based on answers
    total_score = sum(answers)
    num_questions = len(answers)
    average_score = total_score / num_questions

    # Categorize overall mood based on average score and assign emojis
    if average_score <= 2:
        mood_category = "Very Sad"
        mood_emoji = "😞"
    elif 2 < average_score <= 3:
        mood_category = "Sad"
        mood_emoji = "😟"
    elif 3 < average_score <= 4:
        mood_category = "Neutral"
        mood_emoji = "😐"
    elif 4 < average_score <= 5:
        mood_category = "Happy"
        mood_emoji = "😊"

    return mood_category, mood_emoji

#sorts the scores which is used to get the results and advice
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)

#categorize mood based on the score(range)
def categorize_mood(score):
    if score < 10:
        return "Very Sad"
    elif 10 <= score < 20:
        return "Sad"
    elif 20 <= score < 30:
        return "Neutral"
    elif 30 <= score < 40:
        return "Happy"
    
#function that generates advice based on the users mood
def get_advice(category):
    if category == "Very Sad":
        return "Consider talking to a friend or seeking professional help. Do not bottle up your feelings. Getting it out in the open can help you get a lot of weight off your shoulders. Talk to a therapist or if you do not feel comfortable with that talk to a friend. Do not give up and keep on trying."
    elif category == "Sad":
        return "Take a break, listen to music, or engage in activities you enjoy. Try to find something that can bring back some happiness into your life. You deserve to be happy, so do not stop trying to bring your spark back."
    elif category == "Neutral":
        return "You are neither sad or happy. Try taking sometime to yourself and reflecting on this past week. Try to find something that made have made you happy or sad. Talk about it or write about it using our Journal."
    elif category == "Happy":
        return "We are glad you are happy and doing well. Keep doing what makes you happy and spread the positivity. Do not let anything bring you down and keep being you!"
    else:
        return "You're doing great! Keep up the positive vibes." 

#route for the home page
@app.route('/')
def home():
    return render_template('index.html')

#route for the login
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect('users.db') #database that stores the user login info
    c = conn.cursor()

    c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password)) #access the database
    user = c.fetchone()

    conn.close()

    if user:
        return render_template('menu.html', username=username) #going to the menu page if the login information is correct
    else:
        flash('Incorrect username or password', 'error') #error message for wrong username/password
        return redirect(url_for('home'))

@app.route('/register')
def register():
    return render_template('register.html')

# Modified /stressometer route to handle form submissions
@app.route('/stressometer', methods=['GET', 'POST'])
def stressometer():
    if request.method == 'POST':
        # Extracting scores from the form
        scores = [int(request.form[f'q{i}']) for i in range(1, 10)]

        # Sorting the scores using quicksort
        sorted_scores = quicksort(scores)

        # Summing the top 5 scores
        total_score = sum(sorted_scores[-5:])

        # Categorizing the overall mood
        mood_category = categorize_mood(total_score)

        # Calculating mood category and emoji
        mood_category, mood_emoji = calculate_overall_mood(scores)

        # Getting advice based on the mood category
        advice = get_advice(mood_category)

        return render_template('stressometer_result.html', mood_category=mood_category, mood_emoji=mood_emoji, advice=advice)

    return render_template('stressometer.html')


@app.route('/journaling/<username>')
def journaling(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    # Fetch journal entries along with timestamps for the current user
    c.execute('SELECT journal_content, timestamp FROM user_entries WHERE user_id = (SELECT id FROM users WHERE username = ?)', (username,))
    entries = c.fetchall()

    conn.close()
    
    return render_template('journaling.html', username=username, entries=entries)

#route for saving the journal entry
@app.route('/save_journal', methods=['POST'])
def save_journal():
    if request.method == 'POST':
        journal_content = request.form['journal_content']
        username = request.form['username']
        
        # Get current timestamp
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('INSERT INTO user_entries (user_id, journal_content, timestamp) VALUES ((SELECT id FROM users WHERE username = ?), ?, ?)', (username, journal_content, current_time))
        conn.commit()
        conn.close()

        return redirect(url_for('journaling', username=username))
#route for good news
@app.route('/good_news', methods=['GET', 'POST'])
def good_news():
    if request.method == 'POST':
        category = request.form.get('category', 'animals')  # Default to 'animals' if no category is selected
        random_article = get_random_good_news(category)
        return render_template('good_news.html', articles=[random_article])

    # If it's a GET request, show an article from the default category
    default_category = 'animals'
    random_article = get_random_good_news(default_category)
    return render_template('good_news.html', articles=[random_article])

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    conn.commit()

    conn.close()

    flash(f'Account created for {username}', 'success') #flashing message when the user has created an account succesfully
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
