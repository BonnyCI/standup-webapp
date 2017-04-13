from standup_webapp import app

import sqlite3
from datetime import date, timedelta, datetime
from flask import g, render_template, request, redirect, url_for


@app.route('/')
def index():
    """ main entrypoint into flask app. Redirects to today's standup"""
    date_to_show = datetime.today().date()
    params = {"year": date_to_show.year,
              "month": date_to_show.month,
              "day": date_to_show.day}
    return redirect(url_for('show_entries', **params))


@app.route('/show')
def show():
    """ A helper to convert a param-based url '/show?date=YYYY-MM-dd'
         into a path-based one '/YYYY/MM/dd/'.

         This simplifies the 'next/prev' logic in the templates"""

    date_str = request.args.get('date', '')
    date_to_show = datetime.strptime(date_str, '%Y-%m-%d').date()
    params = {"year": date_to_show.year,
              "month": date_to_show.month,
              "day": date_to_show.day}
    return redirect(url_for('show_entries', **params))


@app.route('/<year>/<month>/<day>/')
def show_entries(year, month, day):
    """ main method that gets db info, and renders the page """
    date_to_show, prior_date, next_date = get_dates(year, month, day)
    db = get_db()
    if db is not None:
        cur = db.execute('select id, author, yesterday, today, blockers from statuses where date=? order by id desc', (date_to_show, ))
        entries = cur.fetchall()
        return render_template('show_entries.html', entries=entries, date_to_show=date_to_show.strftime("%A %Y-%m-%d"), prior_date=prior_date, next_date=next_date)
    else:
        return render_template('no_database.html')


def connect_db():
    """Connects to the specific database."""
    try:
        conn = sqlite3.connect(app.config['DATABASE'])
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.OperationalError:
        return None


def get_db():
    if not hasattr(g, '_database'):
        g._database = connect_db()
    return g._database


@app.teardown_appcontext
def close_connection(exception):
    if hasattr(g, '_database'):
        if g._database is not None:
            g._database.close()


def get_dates(year, month, day):
    """ determines next and prior weekdays,
        and creates datetime objects for each"""
    year, month, day = int(year), int(month), int(day)
    date_to_show = date(year, month, day)
    if date_to_show.weekday() > 0:  # ignore weekend
        prior_date = date_to_show - timedelta(days=1)
    else:
        prior_date = date_to_show - timedelta(days=3)

    if date_to_show.weekday() < 4:  # ignore weekend
        next_date = date_to_show + timedelta(days=1)
    else:
        next_date = date_to_show + timedelta(days=3)
    return (date_to_show, prior_date, next_date)


if __name__ == "__main__":
    app.run()
