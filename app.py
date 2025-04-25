from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
DATA_FILE = 'stories.json'

def load_stories():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_story(story):
    stories = load_stories()
    stories.append(story)
    with open(DATA_FILE, 'w') as f:
        json.dump(stories, f, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        story = {
            'title': request.form['title'],
            'tag': request.form['tag'],
            'content': request.form['content']
        }
        save_story(story)
        return redirect(url_for('view_stories'))
    return render_template('add.html')

@app.route('/view')
def view_stories():
    stories = load_stories()
    return render_template('view.html', stories=stories)

if __name__ == '__main__':
    app.run(debug=True)
