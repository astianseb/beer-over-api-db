#!/bin/python

# from flask import Flask, jsonify, request, render_template
import uuid
import random
# from sqlite3 import dbapi2 as sqlite3
# import os
import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash, jsonify

# Initialize the Flask application
BATCH_NUMBER = 0

app = Flask(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'beer.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def close_db():
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


# This route will return a list in JSON format
@app.route('/')
def index():
    db = get_db()
    cur = db.execute(
        'select beer_batch_number, beer_number_in_batch, beer_type, beer_id from beer_entries order by id desc')
    entries = cur.fetchall()
    return render_template('index.html', entries=entries, batch_no=BATCH_NUMBER)


@app.route('/brewme')
def clone():
    global BATCH_NUMBER
    BATCH_NUMBER += 1
    given_number = int(request.query_string)
    uuid_list = []
    beer_list = []
    beer_type_list = ["ale", "brown-ale", "IPA", "AIPA", "lager", "wheat"]
    db = get_db()
    for i in range(given_number):
        beer_list = [{"beer_number": i,
                      "beer_type": random.choice(beer_type_list),
                      "beer_ID": str(uuid.uuid4())}]
        db.executemany(
            "insert into beer_entries (beer_batch_number, beer_number_in_batch, beer_type, beer_id) values (?, ?, ?, ?)",
              [(BATCH_NUMBER,
              beer_list[0]['beer_number'],
              beer_list[0]['beer_type'],
              beer_list[0]['beer_ID'])])
        uuid_list.append(beer_list)
    db.commit()
    close_db()
    return jsonify(beer_batch=uuid_list)


if __name__ == '__main__':
    init_db()
    app.run(
        host="0.0.0.0",
        port=int("5000")
    )

