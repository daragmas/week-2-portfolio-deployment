import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from data.profiles import profiles
from peewee import *
import datetime
from playhouse.shortcuts import model_to_dict
from flask_gravatar import Gravatar
import re

load_dotenv(dotenv_path="./.env")
app = Flask(__name__)

gravatar = Gravatar(app,
                    size=60,
                    rating='g',
                    default='identicon',
                    force_default=False,
                    force_lower=False,
                    use_ssl=True,
                    base_url=None)
if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)

else:
    mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
                        user=os.getenv("MYSQL_USER"),
                        password=os.getenv("MYSQL_PASSWORD"),
                        host=os.getenv("MYSQL_HOST"),
                        port=3306
                        )

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb

try:
    mydb.connect()
    mydb.create_tables([TimelinePost])
except InterfaceError as e:
    print(e)

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


@app.route('/timeline')
def timeline():
    timelinePosts = get_time_line_post()['timeline_posts']
    return render_template('timeline.html', title="Timeline", timelinePosts=timelinePosts, gravatar=gravatar)


# ---------- API Routes -----------------

@app.route('/api/timeline_post', methods=["POST"])
def post_time_line_post():
    if 'name' not in request.form or request.form['name'].strip() == "":
        return "Invalid name", 400
    
    if 'email' not in request.form or request.form['email'].strip() == "":
        return "Invalid email", 400
    
    if not re.search(r'(.+?)@(.+?)\.(.+?)', request.form['email']):
        return "Invalid email", 400
    
    if 'content' not in request.form or request.form['content'].strip() == "":
        return "Invalid content", 400
    
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']
    timeline_post = TimelinePost.create(name=name, email=email, content=content)

    return model_to_dict(timeline_post)


@app.route('/api/timeline_post', methods=["GET"])
def get_time_line_post():
    return {
        'timeline_posts': [
            model_to_dict(p) 
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
            ]
    }


@app.route('/api/timeline_post', methods=["DELETE"])
def delete_time_line_post():
    post_id = request.form['post_id']
    deletion = TimelinePost.delete().where(TimelinePost.id == post_id)
    rowsDeleted = deletion.execute()
    if rowsDeleted > 0:
        return {
            "status": "Success",
            "deleted_id": post_id
        }
    else:
        return {
            "status": "Failure",
        }
    
