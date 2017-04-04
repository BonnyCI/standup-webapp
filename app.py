import sqlite3
from flask import Flask, g, render_template

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE='/home/bradonk/code/errbot-testing/data/plugins/standup.sqlite'
))

@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select id, date, author, yesterday, today, blockers from statuses order by id desc')
    entries = cur.fetchall()
    print(entries)
    return render_template('show_entries.html', entries=entries)

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    if not hasattr(g, '_database'):
        g._database = connect_db()
    return g._database

@app.teardown_appcontext
def close_connection(exception):
    if hasattr(g, '_database'):
        g._database.close()

