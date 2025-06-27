import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from data.profiles import profiles

load_dotenv()
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', title="MLH Fellows", url=os.getenv("URL"), profiles=profiles)


@app.route('/hobbies/<name>')
def hobbies(name):
    profile = next(
        (p for p in profiles if p['name'].lower().replace(" ", "-") == name), None)
    return render_template('hobbies.html',
                           profile=profile,
                           title=profile['name'],
                           url=os.getenv("URL"),
                           profiles=profiles)


@app.route('/about/<name>')
def about_profile(name):
    profile = next(
        (p for p in profiles if p['name'].lower().replace(" ", "-") == name), None)
    return render_template('about_page.html',
                           profile=profile,
                           title=profile['name'],
                           url=os.getenv("URL"),
                           profiles=profiles)
