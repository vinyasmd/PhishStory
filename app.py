import os
import random
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///phishstory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Check and remove the old database if it exists
if os.path.exists("phishstory.db"):
    print("Removing old database...")
    os.remove("phishstory.db")

# Define the PhishStory model
class PhishStory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    story = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Create the tables in the DB
with app.app_context():
    print("Creating new database...")
    db.create_all()

# List of cybersecurity quotes
quotes = [
    "Cybersecurity is much more than an IT topic. It’s a business topic.",
    "Security used to be an inconvenience sometimes, but now it’s a necessity all the time.",
    "The best defense against phishing is awareness.",
    "Think before you click!",
    "Your story can help someone stay secure.",
    "Sharing is caring – especially when it comes to cybersecurity!",
    "Stay alert. Stay secure.",
    "Every experience matters. Share yours!",
    "One click can change everything. Share to protect others.",
    "Together we build a safer internet."
]

@app.route('/')
def index():
    stories = PhishStory.query.order_by(PhishStory.timestamp.desc()).all()
    random_quote = random.choice(quotes)
    return render_template('index.html', stories=stories, random_quote=random_quote)

@app.route('/submit', methods=['POST'])
def submit():
    story = request.form['story']
    if story.strip() == '':
        return redirect(url_for('index'))

    new_story = PhishStory(story=story)
    db.session.add(new_story)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    story = PhishStory.query.get_or_404(id)
    db.session.delete(story)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
   app.run(host="0.0.0.0", port=10000)

